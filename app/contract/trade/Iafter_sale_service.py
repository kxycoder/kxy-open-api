# 接口文件 (基于 after_sale_service.py 生成)

from abc import ABC, abstractmethod


class IAfterSaleService(ABC):
    @abstractmethod
    async def GetAfterSaleDetail(self, after_sale_id):
        pass

