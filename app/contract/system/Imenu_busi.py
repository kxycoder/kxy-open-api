# 接口文件 (基于 menu_busi.py 生成)

from abc import ABC, abstractmethod


class IMenuBusi(ABC):
    @abstractmethod
    async def GetBaseUserMenus(self, systemcode, isdisplay):
        pass

    @abstractmethod
    async def GetUserMenus(self, systemcode, isdisplay):
        pass

    @abstractmethod
    async def GetUserMenuAndActions(self, systemcode, isdisplay):
        pass

    @abstractmethod
    async def GetUserPermissions(self, systemcode):
        pass

    @abstractmethod
    async def GetUserMenusAnt(self, systemcode, isdisplay):
        pass

    @abstractmethod
    async def ClearSystemCodeCache(self, systemcode):
        pass

    @abstractmethod
    async def GetUserAllMenus(self, systemcode, userid):
        pass

    @abstractmethod
    async def GetRoleAllMenus(self, systemcode, roleid):
        pass

    @abstractmethod
    async def GetSystemAllMenu(self, systemcode, search = ''):
        pass

    @abstractmethod
    async def GetSystemRoles(self, systemcode, userid):
        pass

    @abstractmethod
    async def GetUserRoles(self, systemcode, userid):
        pass

    @abstractmethod
    async def GetUserRolesId(self, systemcode, userid):
        pass

    @abstractmethod
    async def GetUserRolesIdCache(self, systemcode, userid, clear=False):
        pass

    @abstractmethod
    async def GetUserRolesNameCache(self, systemcode, userid, clear=False):
        pass

    @abstractmethod
    async def GetUserRoleNames(self, systemcode, userid):
        pass

    @abstractmethod
    async def AddSystemCode(self, jsonData):
        pass

    @abstractmethod
    async def CheckPermission(self, systemcode, userId, permissions):
        pass

    @abstractmethod
    async def GetUserVisibleCacheKey(self, systemcode, module, userid):
        pass

    @abstractmethod
    async def GetModuleVisible(self, systemcode, userId, module):
        pass

    @abstractmethod
    async def SaveMenus(self, menus, parentId=0):
        pass

    @abstractmethod
    async def GetSchemaResource(self, systemcode, objecttype, objectid, schemaId, MenuId):
        pass

    @abstractmethod
    async def GetUserResource(self, systemcode, userid, schemaId, MenuId):
        pass

    @abstractmethod
    async def GetRoleResource(self, systemcode, roleId, schemaId, MenuId):
        pass

    @abstractmethod
    async def ChangeSchemaPower(self, systemcode, objecttype, objectid, schemaId, resource):
        pass

    @abstractmethod
    async def ClearRoleResourceCache(self, systemcode, schema, source):
        pass

    @abstractmethod
    async def ClearBatchKey(self, key):
        pass

    @abstractmethod
    async def ClearUserSingleCache(self, systemcode, schema, source, userid):
        pass

    @abstractmethod
    async def ClearUserAllCache(self, systemcode, userid):
        pass

    @abstractmethod
    async def ClearAllUserSystemCache(self, systemcode):
        pass

    @abstractmethod
    async def ChangeUserResourcePower(self, systemcode, userid, schemaId, resource):
        pass

    @abstractmethod
    async def ChangeRoleResourcePower(self, systemcode, roleid, schemaId, resource):
        pass

    @abstractmethod
    async def SyncToRemote(self, systemcode, name, datas):
        pass

    @abstractmethod
    async def SyncMenu(self, systemcode):
        pass

    @abstractmethod
    async def SynMenuRevice(self, jsonData):
        pass

    @abstractmethod
    async def GetUserSystemCodeCacheKey(self, systecode, module, userid):
        pass

    @abstractmethod
    async def GetUserEnabledResource(self, systecode, user_id, Module):
        pass

    @abstractmethod
    async def GetEnabledResource(self, systecode, user_id, Module):
        pass

    @abstractmethod
    async def GetUserEnableSysmteCode(self, userid):
        pass

    @abstractmethod
    async def InitMenu(self, datas):
        pass

    @abstractmethod
    async def InitMenuPermission(self, menuInfo):
        pass

    @abstractmethod
    async def InitSuperAdminMenu(self, systemCode):
        pass

    @abstractmethod
    async def InitMenuPublic(self, datas):
        pass

    @abstractmethod
    async def DeleteMenu(self, id):
        pass

    @abstractmethod
    async def SyncUIMenu(self, jsonData):
        pass

    @abstractmethod
    async def _genUiMenu(self, systemcode, routes, parentId):
        pass

