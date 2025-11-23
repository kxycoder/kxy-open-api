# 接口文件 (基于 config_service.py 生成)

from abc import ABC, abstractmethod


class IConfigService(ABC):
    @abstractmethod
    async def Get(self, key):
        pass

