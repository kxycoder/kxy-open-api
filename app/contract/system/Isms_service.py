# 接口文件 (基于 sms_service.py 生成)

from abc import ABC, abstractmethod


class ISmsService(ABC):
    @abstractmethod
    async def SendByUserId(self, userid, templateCode, **params):
        pass

    @abstractmethod
    async def SendByDetail(self, userId, userType, mobile, templateCode, **params):
        pass

    @abstractmethod
    async def createClient(self, channelInfo):
        pass

    @abstractmethod
    async def GetSender(self, channelId):
        pass

    @abstractmethod
    async def SendByLog(self, sendLog):
        pass

    @abstractmethod
    async def GenerateLog(self, templateCode, userId, userType, mobile, **params):
        pass

    @abstractmethod
    async def AddTemplate(self, jsonData):
        pass

    @abstractmethod
    async def UpdateTemplate(self, jsonData):
        pass

