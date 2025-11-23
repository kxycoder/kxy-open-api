
from app.config import config
from app.system.dal.sys_public_dictionary_dal import SysPublicDictionaryDal
from app.upload.aliyun_file_service import AliyunFileService
from app.upload.file_service_contract import BaseFileService


class FileService():
    client:BaseFileService=None
    def __init__(self):
        pass
    async def createClient(self):
        if FileService.client:
            # logger.info('短信发送客户端已存在，直接返回')
            return FileService.client
        FileService.client = AliyunFileService(config.Cloud_AccessKey,config.Cloud_AccessSecret,config.COS_BucketName,config.COS_Region)
        return FileService.client
    def UploadFile(self,file,fileName):
        return FileService.client.uploadFile(file,fileName)