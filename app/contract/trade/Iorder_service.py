# 接口文件 (基于 order_service.py 生成)

from abc import ABC, abstractmethod


class IOrderService(ABC):
    @abstractmethod
    async def GetOrderList(self, search, PageIndex, PageLimit):
        pass

    @abstractmethod
    async def GetOrderDetail(self, order_id):
        pass

    @abstractmethod
    async def DeliveryOrder(self, order_id, logistics_id, logistics_no, admin_user=None):
        pass

