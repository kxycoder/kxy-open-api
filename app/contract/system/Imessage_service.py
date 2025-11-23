# 接口文件 (基于 message_service.py 生成)

from abc import ABC, abstractmethod


class IMessageService(ABC):
    @abstractmethod
    async def createClient(self):
        pass

    @abstractmethod
    async def SaveAsJson(self, jsonData):
        pass

    @abstractmethod
    async def CloseSendSetting(self, id):
        pass

    @abstractmethod
    async def AddByJson(self, jsonData):
        pass

    @abstractmethod
    async def CloseBirthDayRemind(self, friendId):
        pass

    @abstractmethod
    async def generatParam(self, setting, **args):
        pass

    @abstractmethod
    async def GenerateMsgSetting(self, setting):
        pass

    @abstractmethod
    async def genNextSendTime(self, setting):
        pass

    @abstractmethod
    async def updateNextSendTime(self, setting):
        pass

    @abstractmethod
    async def send_message(self):
        pass

    @abstractmethod
    async def SendToWeChat(self, msg):
        pass

    @abstractmethod
    async def BeginSendsms(self):
        pass

    @abstractmethod
    async def DeleteFriend(self, friendId):
        pass

    @abstractmethod
    async def SendInteralMsg(self, uid, msgType, title, content):
        pass

    @abstractmethod
    async def UserRegist(self, uid):
        pass

    @abstractmethod
    async def Callback(self, jsonData):
        pass

    @abstractmethod
    async def ReadMsgBatch(self, messageIds):
        pass

