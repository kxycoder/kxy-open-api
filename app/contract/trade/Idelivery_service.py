# 接口文件 (基于 delivery_service.py 生成)

from abc import ABC, abstractmethod


class IDeliveryService(ABC):
    @abstractmethod
    async def get_express_template_by_id(self, template_id):
        pass

    @abstractmethod
    async def create_express_template(self, data):
        pass

    @abstractmethod
    async def update_express_template(self, template_id, data):
        pass

    @abstractmethod
    async def delete_express_template(self, template_id):
        pass

    @abstractmethod
    async def bind_verify_users(self, store_id, verify_user_ids):
        pass

    @abstractmethod
    async def get_store(self, store_id):
        pass

