# 接口文件 (基于 tenant_service.py 生成)

from abc import ABC, abstractmethod


class ITenantService(ABC):
    @abstractmethod
    async def RegisteTenant(self, registData):
        pass

    @abstractmethod
    async def CreateTenant(self, tenant):
        pass

    @abstractmethod
    async def init_tenant_roles(self, tenantId, userid, packageId, AutoCommit=True):
        pass

    @abstractmethod
    async def DeleteTenant(self, tenantId):
        pass

    @abstractmethod
    async def UpdatePackage(self, jsonData):
        pass

    @abstractmethod
    async def GetTenantIdPackageCategoryItems(self, categoryName, tenantId):
        pass

    @abstractmethod
    async def GetPackageCategory(self, categoryName):
        pass

