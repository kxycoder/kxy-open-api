from abc import ABC, abstractmethod
from app.infra.models.infra_file_config import InfraFileConfig
import io
import os
import json
import aioboto3
import asyncssh
import aioftp
import aiofiles
from datetime import datetime
from uuid import uuid4
from app.infra.dal.infra_file_dal import InfraFileDal
from app.infra.dal.infra_file_config_dal import InfraFileConfigDal
from app.infra.models.infra_file import InfraFile
from app.system.services.base_service import BaseService
from kxy.framework.friendly_exception import FriendlyException
from app.config import config
from app.database import redisClient
from functools import lru_cache
from typing import Optional
import asyncio

# 全局缓存 master 配置
_master_config = None

# 本地内存缓存配置（用于文件配置的多级缓存）
# 使用字典作为本地缓存，key 为 config_id，value 为 (config_obj, timestamp)
_local_config_cache = {}
_local_cache_lock = asyncio.Lock()
LOCAL_CACHE_EXPIRE = 300  # 本地缓存5分钟
LOCAL_CACHE_MAX_SIZE = 100  # 最多缓存100个配置

# Redis 缓存配置
REDIS_FILE_CONFIG_KEY_PREFIX = "file:config:"
REDIS_FILE_CONFIG_EXPIRE = 3600  # 缓存1小时

async def load_master_config(session):
    global _master_config
    config_dal = InfraFileConfigDal(session)
    _master_config = await config_dal.GetMasterConfig()

def get_master_config():
    global _master_config
    if not _master_config:
        raise FriendlyException("未找到存储配置")
    return _master_config

async def _evict_old_local_cache():
    """
    清理过期的本地缓存，并确保缓存大小不超过限制
    """
    global _local_config_cache
    current_time = datetime.now().timestamp()

    # 清理过期的缓存
    expired_keys = [
        key for key, (_, timestamp) in _local_config_cache.items()
        if current_time - timestamp > LOCAL_CACHE_EXPIRE
    ]
    for key in expired_keys:
        del _local_config_cache[key]

    # 如果缓存数量超过限制，删除最旧的条目（LRU）
    if len(_local_config_cache) >= LOCAL_CACHE_MAX_SIZE:
        # 按时间戳排序，删除最旧的条目
        sorted_items = sorted(_local_config_cache.items(), key=lambda x: x[1][1])
        for key, _ in sorted_items[:len(sorted_items) // 4]:  # 删除25%的旧条目
            del _local_config_cache[key]


async def get_config_from_cache_or_db(session, config_id: int):
    """
    从多级缓存或数据库获取文件配置
    三级缓存策略：本地内存 -> Redis -> 数据库
    :param session: 数据库会话
    :param config_id: 配置ID
    :return: 配置对象
    """
    global _local_config_cache
    current_time = datetime.now().timestamp()

    # 第一级：尝试从本地内存缓存获取
    async with _local_cache_lock:
        if config_id in _local_config_cache:
            config_obj, timestamp = _local_config_cache[config_id]
            # 检查是否过期
            if current_time - timestamp <= LOCAL_CACHE_EXPIRE:
                # 更新访问时间（LRU）
                _local_config_cache[config_id] = (config_obj, current_time)
                return config_obj
            else:
                # 过期则删除
                del _local_config_cache[config_id]

    # 第二级：尝试从 Redis 获取
    redis_key = f"{REDIS_FILE_CONFIG_KEY_PREFIX}{config_id}"
    redis = redisClient
    cached_data = await redis.get_json(redis_key)

    if cached_data:
        # 重新构建配置对象
        config_obj = InfraFileConfig()
        for key, value in cached_data.items():
            setattr(config_obj, key, value)

        # 回填到本地缓存
        async with _local_cache_lock:
            await _evict_old_local_cache()
            _local_config_cache[config_id] = (config_obj, current_time)

        return config_obj

    # 第三级：缓存未命中，从数据库查询
    config_dal = InfraFileConfigDal(session)
    config_obj = await config_dal.Get(config_id)

    if not config_obj:
        raise FriendlyException("未找到存储配置")

    # 将配置对象序列化并存入 Redis
    config_dict = {
        'id': config_obj.id,
        'storage': config_obj.storage,
        'name': config_obj.name,
        'config': config_obj.config,
        'master': config_obj.master,
        'remark': config_obj.remark
    }
    await redis.set_json(redis_key, config_dict, ex=REDIS_FILE_CONFIG_EXPIRE)

    # 同时存入本地缓存
    async with _local_cache_lock:
        await _evict_old_local_cache()
        _local_config_cache[config_id] = (config_obj, current_time)

    return config_obj

async def clear_config_cache(config_id: int):
    """
    清除指定配置的多级缓存（本地内存 + Redis）
    :param config_id: 配置ID
    """
    global _local_config_cache

    # 清除本地内存缓存
    async with _local_cache_lock:
        if config_id in _local_config_cache:
            del _local_config_cache[config_id]

    # 清除 Redis 缓存
    redis_key = f"{REDIS_FILE_CONFIG_KEY_PREFIX}{config_id}"
    redis = redisClient.client
    await redis.delete(redis_key)

class FileStorageClient(ABC):
    @abstractmethod
    async def upload(self, file, config_obj):
        raise NotImplementedError
    @abstractmethod
    async def download(self, config_obj, file_path):
        raise NotImplementedError

class S3FileStorageClient(FileStorageClient):
    async def upload(self, file, config_obj):
        s3_cfg = config_obj.config
        endpoint = s3_cfg.get("endpoint")
        bucket = s3_cfg.get("bucket")
        access_key = s3_cfg.get("accessKey")
        access_secret = s3_cfg.get("accessSecret")
        domain = s3_cfg.get("domain")
        enable_path_style = s3_cfg.get("enablePathStyleAccess", False)
        now = datetime.now()
        ext = file.filename.split('.')[-1]
        file_name = f'{now.year}{now.month}{now.day}/{uuid4()}.{ext}'

        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=f"http://{endpoint}" if not endpoint.startswith("http") else endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=access_secret,
        ) as s3:
            file.file.seek(0)
            await s3.upload_fileobj(file.file, bucket, file_name)

        url = f"{domain}/{config.BackEndPrefix}/infra/file/{config_obj.id}/get/{file_name}"
        return file_name, url

    async def download(self, config_obj, file_path):
        s3_cfg = config_obj.config
        endpoint = s3_cfg.get("endpoint")
        bucket = s3_cfg.get("bucket")
        access_key = s3_cfg.get("accessKey")
        access_secret = s3_cfg.get("accessSecret")

        session = aioboto3.Session()
        file_stream = io.BytesIO()
        try:
            async with session.client(
                's3',
                endpoint_url=f"http://{endpoint}" if not endpoint.startswith("http") else endpoint,
                aws_access_key_id=access_key,
                aws_secret_access_key=access_secret,
            ) as s3:
                await s3.download_fileobj(bucket, file_path, file_stream)
            file_stream.seek(0)
            return file_stream.read()
        except Exception as e:
            if hasattr(e, 'response') and e.response.get('Error', {}).get('Code') == 'InvalidObjectState':
                raise FriendlyException("S3文件当前状态不支持下载（如为归档存储），请先解冻或检查存储类型")
            raise FriendlyException(f"S3文件下载失败: {str(e)}")

class SftpFileStorageClient(FileStorageClient):
    async def upload(self, file, config_obj):
        cfg = config_obj.config
        host = cfg.get("host")
        port = cfg.get("port", 22)
        username = cfg.get("username")
        password = cfg.get("password")
        base_path = cfg.get("basePath")
        domain = cfg.get("domain")
        now = datetime.now()
        ext = file.filename.split('.')[-1]
        file_name = f'{now.year}{now.month}{now.day}/{uuid4()}.{ext}'
        remote_path = os.path.join(base_path, file_name)

        async with asyncssh.connect(host, port=port, username=username, password=password, known_hosts=None) as conn:
            async with conn.start_sftp_client() as sftp:
                # 确保目录存在
                dir_path = os.path.dirname(remote_path)
                try:
                    await sftp.makedirs(dir_path)
                except:
                    pass  # 目录可能已存在
                file.file.seek(0)
                await sftp.put(file.file, remote_path)

        url = f"{domain}/{config.BackEndPrefix}/infra/file/{config_obj.id}/get/{file_name}"
        return file_name, url

    async def download(self, config_obj, file_path):
        cfg = config_obj.config
        host = cfg.get("host")
        port = cfg.get("port", 22)
        username = cfg.get("username")
        password = cfg.get("password")
        base_path = cfg.get("basePath")
        remote_path = os.path.join(base_path, file_path)

        try:
            async with asyncssh.connect(host, port=port, username=username, password=password, known_hosts=None) as conn:
                async with conn.start_sftp_client() as sftp:
                    file_stream = io.BytesIO()
                    await sftp.get(remote_path, file_stream)
                    file_stream.seek(0)
                    return file_stream.read()
        except Exception as e:
            raise FriendlyException(f"SFTP文件下载失败: {str(e)}")

class FtpFileStorageClient(FileStorageClient):
    async def upload(self, file, config_obj):
        cfg = config_obj.config
        host = cfg.get("host")
        port = cfg.get("port", 21)
        username = cfg.get("username")
        password = cfg.get("password")
        base_path = cfg.get("basePath")
        domain = cfg.get("domain")
        now = datetime.now()
        ext = file.filename.split('.')[-1]
        file_name = f'{now.year}{now.month}{now.day}/{uuid4()}.{ext}'
        relative_path = f'{now.year}{now.month}{now.day}'

        async with aioftp.Client.context(host, port, username, password) as client:
            # 确保目录存在
            try:
                await client.change_directory(base_path)
                await client.make_directory(relative_path)
            except:
                pass  # 目录可能已存在

            await client.change_directory(base_path)
            await client.change_directory(relative_path)
            file.file.seek(0)
            await client.upload_stream(file.file, f'{uuid4()}.{ext}')

        url = f"{domain}/{config.BackEndPrefix}/infra/file/{config_obj.id}/get/{file_name}"
        return file_name, url

    async def download(self, config_obj, file_path):
        cfg = config_obj.config
        host = cfg.get("host")
        port = cfg.get("port", 21)
        username = cfg.get("username")
        password = cfg.get("password")
        base_path = cfg.get("basePath")

        file_stream = io.BytesIO()
        try:
            async with aioftp.Client.context(host, port, username, password) as client:
                await client.change_directory(base_path)
                await client.download_stream(file_path, file_stream)
            file_stream.seek(0)
            return file_stream.read()
        except Exception as e:
            raise FriendlyException(f"FTP文件下载失败: {str(e)}")

class LocalFileStorageClient(FileStorageClient):
    async def upload(self, file, config_obj):
        cfg = config_obj.config
        base_path = cfg.get("basePath")
        domain = cfg.get("domain")
        now = datetime.now()
        ext = file.filename.split('.')[-1]
        file_name = f'{now.year}{now.month}{now.day}/{uuid4()}.{ext}'
        local_path = os.path.join(base_path, file_name)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        file.file.seek(0)
        async with aiofiles.open(local_path, 'wb') as f:
            await f.write(file.file.read())
        url = f"{domain}/{config.BackEndPrefix}/infra/file/{config_obj.id}/get/{file_name}"
        return file_name, url

    async def download(self, config_obj, file_path):
        cfg = config_obj.config
        base_path = cfg.get("basePath")
        local_path = os.path.join(base_path, file_path)
        try:
            async with aiofiles.open(local_path, 'rb') as f:
                return await f.read()
        except Exception as e:
            raise FriendlyException(f"本地文件下载失败: {str(e)}")

def get_storage_client(storage_type):
    if storage_type == 20:
        return S3FileStorageClient()
    elif storage_type == 12:
        return SftpFileStorageClient()
    elif storage_type == 11:
        return FtpFileStorageClient()
    elif storage_type == 10:
        return LocalFileStorageClient()
    else:
        raise FriendlyException("不支持的存储类型")

class FileService(BaseService):
    async def upload(self, file):
        # 直接用缓存配置
        config_obj = get_master_config()
        storage_type = config_obj.storage
        client = get_storage_client(storage_type)
        file_name, url = await client.upload(file, config_obj)
        dal = InfraFileDal(self.session)
        file_size = file.size if hasattr(file, 'size') else None
        file_type = file.content_type if hasattr(file, 'content_type') else None
        file_entity = {
            "configId": config_obj.id,
            "name": file.filename,
            "path": file_name,
            "url": url,
            "type": file_type,
            "size": file_size
        }
        await dal.AddByJsonData(file_entity)
        return url

    async def get(self, configType: int, filePath):
        """
        下载文件
        :param configType: 配置ID（可为空，为空时使用默认主配置）
        :param filePath: 文件路径
        :return: 文件二进制数据
        """
        # 根据 configType 获取配置（使用 Redis 缓存）
        if configType is None:
            # 使用默认主配置（内存缓存）
            config_obj = get_master_config()
        else:
            # 从 Redis 缓存或数据库获取指定配置
            config_obj = await get_config_from_cache_or_db(self.session, configType)

        storage_type = config_obj.storage
        client = get_storage_client(storage_type)
        return await client.download(config_obj, filePath)

    async def UpdateDeafultUploadConfig(self, configId: int):
        dal = InfraFileConfigDal(self.session)
        await dal.UpdateMaster(configId)
        # 更新内存缓存
        await load_master_config(self.session)
        # 清除 Redis 缓存
        await clear_config_cache(configId)