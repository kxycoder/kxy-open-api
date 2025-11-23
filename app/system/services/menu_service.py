import traceback
from app.common.auth import IsSuperAdmin
from app.contract.system.Iuser_service import IUserService
from app.system.dal.system_menu_dal import SystemMenuDal
from app.system.dal.system_role_menu_dal import SystemRoleMenuDal
from app.system.services.base_service import BaseService
from app.tools import utils
from kxy.framework.mapper import Mapper
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

class MenuService(BaseService):
    async def InitMenu(self):
        dal = SystemMenuDal(self.session)
        menus = await dal.GetAllMenu()
        rows = utils.tree(menus)
        for row in rows:
            await self.CheckMenuShow(row)
    async def CheckMenuShow(self,menuJson):
        print(menuJson)
        menuType = menuJson.get('type')
        if menuType==3:
            return
        dal = SystemMenuDal(self.session)
        children = menuJson.get('children')
        hasShowBtn = False
        if children:
            for child in children:
                childType = child.get('type')
                if childType!=3:
                    await self.CheckMenuShow(child)
                if childType==3 and child.get('permission')=='/':
                    hasShowBtn = True
        if not hasShowBtn:
            await dal.AddMenuShowBtn(menuJson.get('id'))
    
    async def GetUserMenuAndActions(self):
        try:
            userSvc = Mapper.getservice_by_contract(IUserService,self.session)
            # 获取用户角色ID
            # 获取角色菜单
            menuIds = []
            if IsSuperAdmin():
                menuIds = await SystemRoleMenuDal(self.session).GetRolesMenuId(None)
            else:
                userRoleIds = await userSvc.GetUserRoleIds(self.user_id)
                menuIds =await SystemRoleMenuDal(self.session).GetRolesMenuId(userRoleIds)
            if not menuIds:
                return []
            menus = await SystemMenuDal(self.session).GetMenuByIds(menuIds)
            # 提取权限Key
            permissions = [menu.permission for menu in menus if menu.permission]
            # 获取菜单树
            canShowMenus = [menu.parentId for menu in menus if menu.type==3 and menu.permission=='/']
            treeMenus = [menu for menu in menus if menu.type in [1,2] and menu.id in canShowMenus]
            # 获取用户角色名称
            userRoleNames = await userSvc.GetUserRolesNameCache(self.user_id)
            userInfo = await userSvc.GetUserInfo()
            result ={
                'menus': utils.tree(treeMenus),
                'permissions':permissions,
                'roles':userRoleNames,
                'user':userInfo.to_mini_dict()
                }
            return result
        except Exception as ex:
            logger.error(traceback.format_exc(limit=5))
            raise ex

    async def GetUserMenu(self,clearCache=False):
        if IsSuperAdmin():
            return await SystemMenuDal(self.session).GetSimpleList({})
        userSvc = Mapper.getservice_by_contract(IUserService,self.session)
        userRoleIds = await userSvc.GetUserRoleIds(self.user_id)
        menuIds =await SystemRoleMenuDal(self.session).GetRolesMenuId(userRoleIds)
        if not menuIds:
            return []
        menus = await SystemMenuDal(self.session).GetMenuByIds(menuIds)
        return menus

    async def Delete(self, id):
        """
        删除菜单，级联删除子菜单和所有关联的角色菜单配置
        """
        from app.system.models.system_role_menu import SystemRoleMenu

        try:
            menu_dal = SystemMenuDal(self.session)
            role_menu_dal = SystemRoleMenuDal(self.session)

            # 1. 获取当前菜单及其所有子菜单的ID
            child_menu_ids = await menu_dal.GetMenuAndChildMenu([id])
            all_menu_ids = child_menu_ids + [id]

            logger.info(f"准备删除菜单ID: {id}, 包含子菜单: {child_menu_ids}")

            # 2. 删除所有关联的角色菜单配置（SystemRoleMenu表中的记录）
            await role_menu_dal.DeleteWhere([SystemRoleMenu.menuId.in_(all_menu_ids)])
            logger.info(f"已删除关联的角色菜单配置，菜单IDs: {all_menu_ids}")

            # 3. 删除菜单及其子菜单
            await menu_dal.DeleteBatch(all_menu_ids)
            logger.info(f"已删除菜单及子菜单，共{len(all_menu_ids)}条记录")

        except Exception as ex:
            logger.error(f"删除菜单失败: {str(ex)}")
            logger.error(traceback.format_exc(limit=5))
            raise ex
