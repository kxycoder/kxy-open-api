# 接口文件 (基于 back_ground_service.py 生成)

from abc import ABC, abstractmethod


class IBackGroundService(ABC):
    @abstractmethod
    async def init_message_service():
        pass

    @abstractmethod
    async def init_system():
        pass

    @abstractmethod
    async def send_message_task():
        pass

    @abstractmethod
    async def send_interal_message(uid, title, content):
        pass

    @abstractmethod
    async def update_birthday_sending_task(uid, friendId):
        pass

    @abstractmethod
    async def update_moment_sending_task(uid, momentId):
        pass

    @abstractmethod
    async def user_regist(uid):
        pass

