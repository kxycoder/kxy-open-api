# file:/myspace/source/kxy/kxy.sso.api/app/services/batch_syslog_service.py
import asyncio
from datetime import datetime, timedelta
from app.system.dal.sys_log_dal import SysLogDal
from app.database import AsyncSessionLocal
from app.system.models.sys_log import SysLog
from app.system.services.base_service import BaseService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

class BatchSysLogService():
    _instance_lock = asyncio.Lock()
    _initialized = False
    _batch_queue = asyncio.Queue()
    
    def __new__(cls, *args, **kwargs):
        """实现单例模式"""
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._batch_size = 5
            self._flush_interval = 30  # 5分钟
            self._task = asyncio.create_task(self._background_task())
            self._initialized = True

    async def _background_task(self):
        """后台任务定期处理日志"""
        while True:
            try:
                # 等待第一个日志或超时
                if self._batch_queue.empty():
                    await asyncio.sleep(1)
                    continue
                
                # 收集日志
                batch = []
                try:
                    # 尝试获取最多5条日志
                    for _ in range(self._batch_size):
                        log_item = await asyncio.wait_for(
                            self._batch_queue.get(), 
                            timeout=0.1
                        )
                        batch.append(log_item)
                except asyncio.TimeoutError:
                    pass
                
                # 执行批量写入
                if batch:
                    await self._addBatchLog(batch)
                    
                # 按时间间隔检查
                await asyncio.sleep(self._flush_interval)
                
            except Exception as e:
                # 记录异常日志
                logger.error(f"日志批量写入异常: {str(e)}")

    async def AddLogAsync(self, tableName, action, data):
        """异步添加日志"""
        log_item = {
            "TableName": tableName,
            "Action": action,
            "Data": data,
            "ActionDate": datetime.now()
        }
        await self._batch_queue.put(log_item)

    async def flush(self):
        """强制刷新剩余日志"""
        while not self._batch_queue.empty():
            batch = []
            for _ in range(min(self._batch_size, self._batch_queue.qsize())):
                batch.append(self._batch_queue.get_nowait())
            if batch:
                await self._addBatchLog(batch)
    async def _addBatchLog(self,logs:list):
        async with AsyncSessionLocal() as session:
            try:
                entities = []
                for log in logs:
                    entity = SysLog()
                    entity.InitInsertEntityWithJson(log)
                    entity.CreateUser = 'system'
                    entity.CreateDate = datetime.now()
                    entities.append(entity)
                    session.add(entity)
                await session.commit()
            except Exception as ex:
                await session.rollback()
                logger.error(f"批量插入失败: {str(ex)}")