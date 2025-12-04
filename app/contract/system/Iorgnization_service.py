# 接口文件 (基于 orgnization_service.py 生成)

from abc import ABC, abstractmethod


class IOrgnizationService(ABC):
    @abstractmethod
    async def initialize_user_system_util(cls, session):
        pass

    @abstractmethod
    async def sync_wechat_departments_to_system_dept(self):
        pass

    @abstractmethod
    async def sync_wechat_users_to_system_users(self):
        pass

    @abstractmethod
    async def delete_departments_with_children(self, dept_ids):
        pass
