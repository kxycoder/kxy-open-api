import traceback
from typing import Any, List
from kxy.framework.friendly_exception import FriendlyException
from sqlalchemy import select
from sqlalchemy.orm import load_only
from app.contract.infra.Iconfig_service import IConfigService
from app.contract.system.Iuser_service import IUserService
from app.contract.types.user_vo import VoUserRole, VoUserTenant
from app.system.api.types.vo_request import VoRegistTenant
from app.system.dal.system_menu_dal import SystemMenuDal
from app.system.dal.system_package_category_dal import SystemPackageCategoryDal
from app.system.dal.system_package_setting_dal import SystemPackageSettingDal
from app.system.dal.system_role_dal import SystemRoleDal
from app.system.dal.system_role_menu_dal import SystemRoleMenuDal
from app.system.dal.system_tenant_dal import SystemTenantDal
from app.system.dal.system_tenant_package_dal import SystemTenantPackageDal
from app.system.dal.system_user_role_dal import SystemUserRoleDal
from app.system.dal.system_users_dal import SystemUsersDal
from app.system.models.system_package_category import SystemPackageCategory
from app.system.models.system_tenant import SystemTenant
from app.system.models.system_tenant_package import SystemTenantPackage
from app.system.services.base_service import BaseService
from kxy.framework.mapper import Mapper

from app.tools import utils

class TenantService(BaseService):
    async def RegisteTenant(self,registData:VoRegistTenant):
        dal = SystemUsersDal(self.session)
        configSvc = Mapper.getservice_by_contract(IConfigService,self.session)
        register_enabled= await configSvc.Get('system.user.register-enabled')
        if register_enabled != 'true':
            raise FriendlyException("系统未开放注册")
        default_tenant_package =await configSvc.Get('default_tenant_package')
        if not default_tenant_package:
            raise FriendlyException("请先配置默认租户套餐")
        default_tenant_package = int(default_tenant_package)
        tenant = VoUserTenant(name=registData.tenantName,username=registData.username,contactName=registData.nickname,contactMobile='',password=registData.password,packageId=default_tenant_package)
        userInfo = await self.CreateTenant(tenant)
        userService = Mapper.getservice_by_contract(IUserService,self.session)
        # return await userService.Login(tenant.username,tenant.password)
        # refreshToken  accessToken
        token =await userService.GenerateTenantAccessToken(userInfo,userInfo.tenantId)
        return {
            "userId": userInfo.id,
            "accessToken": token.accessToken,
            "refreshToken": token.refreshToken,
            "expiresTime": 1754036950266
        }
    async def CreateTenant(self,tenant:VoUserTenant):
        AutoCommit = True
        # async with self.session.begin():
        userDal = SystemUsersDal(self.session,AutoCommit=AutoCommit)
        exist = await userDal.GetUserName(tenant.username)
        if exist:
            raise FriendlyException("用户名已存在")
        dal = SystemTenantDal(self.session,AutoCommit=AutoCommit)
        tenantInfo = await dal.AddTenant(tenant)
        userInfo = await userDal.AddUser(tenant.username,tenant.contactName,tenant.password,tenant.contactMobile,tenantInfo.id)
        tenantInfo.contactUserId = userInfo.id
        await dal.Update(tenantInfo)
        await self.init_tenant_roles(tenantInfo.id,userInfo.id,tenant.packageId,AutoCommit)
        return userInfo
    async def init_tenant_roles(self,tenantId,userid,packageId,AutoCommit=True):
        exist = await SystemTenantPackageDal(self.session,AutoCommit=AutoCommit).GetExist(packageId)
        if exist:
            menuIds = exist.menuIds
            if not menuIds:
                raise FriendlyException("租户套餐未配置菜单")
            role = await SystemRoleDal(self.session,AutoCommit=AutoCommit).InitTenantAdminRole(tenantId)
            await SystemRoleMenuDal(self.session,AutoCommit=AutoCommit).AssignRoleMenus(role.id,menuIds,tenantId)
            roleInfo= VoUserRole(roleIds=[role.id],userId=userid)
            await SystemUserRoleDal(self.session,AutoCommit=AutoCommit).AssignUserRole(roleInfo,tenantId)
    async def DeleteTenant(self,tenantId:int):
        try:
            async with self.session.begin():
                dal = SystemTenantDal(self.session,AutoCommit=False)
                exist = await dal.GetExist(tenantId)
                if exist.packageId == 0:
                    raise FriendlyException("内置租户不能删除")
                await dal.Delete(tenantId)
                await SystemUsersDal(self.session,AutoCommit=False).DeleteByTenantId(tenantId)
                await SystemRoleDal(self.session,AutoCommit=False).DeleteByTenantId(tenantId)
                await SystemRoleMenuDal(self.session,AutoCommit=False).DeleteByTenantId(tenantId)
                await SystemUserRoleDal(self.session,AutoCommit=False).DeleteByTenantId(tenantId)
        except Exception as e:
            traceback.print_exc()
            raise e
    # async def UpdateTenantUser(self,)
    async def UpdatePackage(self,jsonData):
        async with self.session.begin():
            dal = SystemTenantPackageDal(self.session,AutoCommit=False)
            packageId = jsonData.get('id')
            exist = await dal.GetExist(packageId)
            exist.InitUpdateFiles(jsonData)
            tenantUsers = await SystemTenantDal(self.session,AutoCommit=False).GetByPackageId(packageId)
            if tenantUsers:
                tenantIds = [tenantUser.id for tenantUser in tenantUsers]
                roles = await SystemRoleDal(self.session,AutoCommit=False).GetAdminRolesByTenantIds(tenantIds)
                roles_dict = {role.tenantId:role for role in roles}
                for tenantUser in tenantUsers:
                    role = roles_dict.get(tenantUser.id)
                    if not role:
                        continue
                    await SystemRoleMenuDal(self.session,AutoCommit=False).AssignRoleMenus(role.id,exist.menuIds,tenantUser.id)
            await dal.Update(exist)
    async def GetTenantIdPackageCategoryItems(self,categoryName,tenantId)->List[Any]:
        # todo 缓存
        categoryInfo = await SystemPackageCategoryDal(self.session).GetByName(categoryName)
        model = utils.loadClass(categoryInfo.tableModel)
        fil = []
        if tenantId!=1:
            tenantInfo = await SystemTenantDal(self.session).GetExist(tenantId)
            ids = await SystemPackageSettingDal(self.session).GetCategorySetting(categoryName,tenantInfo.packageId)
            if not ids:
                return []
            fil.append(model.id.in_(ids))
        if hasattr(model, 'deleted'):
            fil.append(model.deleted==0)
        query = select(model).filter(*fil)
        query = query.options(load_only(*model.get_mini_fields()))
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def GetPackageCategory(self,categoryName)->tuple[SystemPackageCategory]:
        entity =await SystemPackageCategoryDal(self.session).GetByName(categoryName)
        model = utils.loadClass(entity.tableModel)
        fil = []
        if hasattr(model, 'tenantId'):
            fil.append(model.tenantId==1)
        if hasattr(model, 'deleted'):
            fil.append(model.deleted==0)
        query = select(model).filter(*fil)
        query = query.options(load_only(model.id,getattr(model,entity.showField)))
        result = await self.session.execute(query)
        items = result.scalars().all()
        # ids = await SystemPackageSettingDal(self.session).GetCategorySetting(entity.name,packageId)
        return items