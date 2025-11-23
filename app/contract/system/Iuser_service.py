# 接口文件 (基于 user_service.py 生成)

from abc import ABC, abstractmethod


class IUserService(ABC):
    @abstractmethod
    async def LoginWx(self, code, sourceUser='', sourceId='', sourceType=''):
        pass

    @abstractmethod
    async def UpdateUserPhone(self, code):
        pass

    @abstractmethod
    async def GenerateToken(self, user):
        pass

    @abstractmethod
    async def GenerateTenantAccessToken(self, user, tenantId=1):
        pass

    @abstractmethod
    async def RefreshToken(self, refreshTokenInfo):
        pass

    @abstractmethod
    async def GenerateAccessToken(self, user, tenantId=1):
        pass

    @abstractmethod
    async def Login(self, phoneNumber, password):
        pass

    @abstractmethod
    async def GetUserInfo(self):
        pass

    @abstractmethod
    async def RegistUser(self, userName, password, phone):
        pass

    @abstractmethod
    async def UpdateUserInfo(self, userInfo):
        pass

    @abstractmethod
    async def Logout(self):
        pass

    @abstractmethod
    async def GetMyPerrmission(self, userid):
        pass

    @abstractmethod
    async def CheckSchema(self, userid, schema):
        pass

    @abstractmethod
    async def GetUserRoleIds(self, userid):
        pass

    @abstractmethod
    async def GetUserRolesNameCache(self, userid, clearCache=False):
        pass

    @abstractmethod
    async def GetUserMenu(self, clearCache=False):
        pass

    @abstractmethod
    async def GetUserMenuAndActions(self):
        pass

    @abstractmethod
    async def DeleteUser(self, userid):
        pass

    @abstractmethod
    async def UpdateUserStatus(self, id, status):
        pass

    @abstractmethod
    async def AssignUserRole(self, roles):
        pass

    @abstractmethod
    async def DeleleteAccessToken(self, accessToken):
        pass

    @abstractmethod
    async def GetUserById(self, userId):
        pass

