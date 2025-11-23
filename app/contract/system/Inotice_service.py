# 接口文件 (基于 notice_service.py 生成)

from abc import ABC, abstractmethod


class INoticeService(ABC):
    @abstractmethod
    async def SendNotifyMessage(self, userid, user_type, templateCode, **args):
        pass

