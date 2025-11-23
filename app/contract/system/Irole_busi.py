# 接口文件 (基于 role_busi.py 生成)

from abc import ABC, abstractmethod


class IRoleBusi(ABC):
    @abstractmethod
    async def GetSystemUserRoles(self, systemcode, userid):
        pass

