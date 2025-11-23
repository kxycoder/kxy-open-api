# 接口文件 (基于 role_domain.py 生成)

from abc import ABC, abstractmethod


class IRoleDomain(ABC):
    @abstractmethod
    async def ChangeUserRoles(self, systemcode, userid, user_roleIds):
        pass

    @abstractmethod
    async def ChangeUsersRoles(self, systemcode, userids, user_roleIds):
        pass

