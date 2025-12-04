# 接口文件 (基于 config_service.py 生成)

from abc import ABC, abstractmethod


class IConfigService(ABC):
    @abstractmethod
    def watch(key, callback):
        pass

    @abstractmethod
    async def Get(self, key):
        pass

    @abstractmethod
    async def GetByCache(self, key, ex=3600):
        pass

    @abstractmethod
    async def update(self, data):
        pass

