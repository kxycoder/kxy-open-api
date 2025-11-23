from app.system.services.base_service import BaseService
from app.system.services.menu_busi import MenuBusi
from app.system.dal.sys_role_dal import SysRoleDal
from app.system.dal.sys_role_user_dal import SysRoleUserDal
from app.database import get_redis_client

class RoleDomain(BaseService):
    def __init__(self, session,**kwargs):
        super().__init__(session,**kwargs)
        self.redis_client = get_redis_client()
    async def ChangeUserRoles(self,systemcode,userid,user_roleIds):
        dal=SysRoleUserDal(self.session)
        mBusi=MenuBusi(self.session)
        exist_roles=await mBusi.GetUserRoles(systemcode,userid)
        for role in exist_roles:
            if role.RoleId not in user_roleIds:
                await dal.Delete(role.Id)
            else:
                user_roleIds.remove(role.RoleId)
        for id in user_roleIds:
            await dal.AddByFields(id,userid)
        await mBusi.ClearUserAllCache(systemcode,userid)
    async def ChangeUsersRoles(self,systemcode,userids,user_roleIds):
        dal=SysRoleUserDal(self.session)
        mBusi=MenuBusi(self.session)
        for userid in userids:
            exist_roles=await mBusi.GetUserRolesId(systemcode,userid)            
            for role in user_roleIds:
                if role not in exist_roles:
                    await dal.AddByFields(role,userid)
            await mBusi.ClearUserAllCache(systemcode,userid)