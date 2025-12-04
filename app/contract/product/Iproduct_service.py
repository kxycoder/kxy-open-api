# 接口文件 (基于 product_service.py 生成)

from abc import ABC, abstractmethod


class IProductService(ABC):
    @abstractmethod
    async def GetSpuDetail(self, id):
        pass

    @abstractmethod
    async def UpdateByJsonData(self, jsonData):
        pass

    @abstractmethod
    async def GetCommentList(self, search, PageIndex, PageLimit):
        pass

