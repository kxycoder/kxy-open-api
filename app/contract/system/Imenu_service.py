# 接口文件 (基于 menu_service.py 生成)

from abc import ABC, abstractmethod


class IMenuService(ABC):
    @abstractmethod
    async def InitMenu(self):
        pass

    @abstractmethod
    async def CheckMenuShow(self, menuJson):
        pass

    @abstractmethod
    async def GetUserMenuAndActions(self):
        pass

    @abstractmethod
    async def GetUserMenu(self, clearCache=False):
        pass

