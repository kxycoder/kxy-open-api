from os import system

from app.system.dal.sys_menu_dal import SysMenuDal
from app.system.dal.sys_permission_dal import SysPermissionDal

from app.system.dal.sys_role_user_dal import SysRoleUserDal
from app.system.dal.sys_role_dal import SysRoleDal
from app.system.services.base_service import BaseService
class RoleBusi(BaseService):
    async def GetSystemUserRoles(self,systemcode,userid):
        roleDal=SysRoleDal(self.session)
        allroles=await roleDal.GetSystemRoles(systemcode)

        userDal=SysRoleUserDal(self.session)
        return await userDal.GetSystemAndUserRoles(userid,systemcode)
    

