# 接口文件 (基于 dict_service.py 生成)

from abc import ABC, abstractmethod


class IDictService(ABC):
    @abstractmethod
    async def Delete(self, dictId):
        pass

    @abstractmethod
    async def DeleteBatch(self, keys):
        pass

    @abstractmethod
    async def AddDictDataByJson(self, jsonData):
        pass

    @abstractmethod
    async def SaveAll(self, jsonData):
        pass

