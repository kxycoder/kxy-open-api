import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.common.auth import IsSuperAdmin
from app.system.models.system_menu import SystemMenu
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemMenuDal(MyBaseDal[SystemMenu]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemMenu,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemMenu],int]:
        fil = list()
        fil.append(SystemMenu.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemMenu,k) and v:
                fil.append(getattr(SystemMenu,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemMenu.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemMenu.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemMenu.DicType.ilike("%" + search_text + "%"),
            #                  SystemMenu.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemMenu.status == int(status))
        items, total_count = await self.paginate_query(fil, SystemMenu.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemMenu],int]:
        fil = list()
        fil.append(SystemMenu.UID == self.UserId)
        fil.append(SystemMenu.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemMenu.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemMenu.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemMenu.status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemMenu.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index=1, page_size=5000)->List[SystemMenu]:
        fil = list()
        fil.append( SystemMenu.deleted == 0)
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemMenu.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemMenu.status == int(status))
        items = await self.page_fields_nocount_query( SystemMenu.get_mini_fields(), fil,  SystemMenu.sort.asc(), page_index, page_size)
        return items
    async def GetAllMenu(self)->List[SystemMenu]:
        items = await self.QueryWhere([SystemMenu.deleted==0],SystemMenu.get_mini_fields())
        return items
    async def AddByJsonData(self, jsonData)->SystemMenu:
        entity = SystemMenu()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.status = 0
        entity.deleted = 0
        if not IsSuperAdmin() and entity.permission=='/':
            raise FriendlyException('权限/为保留权限，用于菜单展示控制，不能手动添加')
        await self.Insert(entity)
        if entity.type in [1,2]:
            await self.AddMenuShowBtn(entity.id)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemMenu:
        entity = SystemMenu()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemMenu:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        if not IsSuperAdmin() and jsonData.get('permission',None)=='/':
            raise FriendlyException('权限/为保留权限，用于菜单展示控制，不能手动调整')
        entity:SystemMenu=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        menuIds = await self.GetMenuAndChildMenu([id])
        menuIds.append(id)
        await self.DeleteBatch(menuIds)

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemMenu.id.in_(ids)])

    async def GetList(self, search)->List[SystemMenu]:
        fil = [SystemMenu.deleted==0]
        for k,v in search.items():
            if hasattr(SystemMenu,k) and v:
                fil.append(getattr(SystemMenu,k).ilike(f'%{v}%'))
        return await self.QueryWhere(fil,fields=SystemMenu.get_mini_fields(),orderBy=SystemMenu.sort.asc())
    async def GetMenuSchemas(self,menuIds)->List[str]:
        menus = await self.QueryWhere([SystemMenu.id.in_(menuIds),SystemMenu.deleted==0])
        return [x.permission for x in menus]
    async def GetMenuBySchemas(self,schemas)->List[SystemMenu]:
        return await self.QueryWhere([or_(SystemMenu.permission.in_(schemas),SystemMenu.permission==None,SystemMenu.permission==''),SystemMenu.deleted==0])
    async def GetMenuByIds(self,ids)->List[SystemMenu]:
        return await self.QueryWhere([SystemMenu.id.in_(ids),SystemMenu.status==0,SystemMenu.deleted==0],orderBy=SystemMenu.sort.asc())
    async def GetMenuAndChildMenu(self,menuIds):
                # 一次性获取所有未删除的菜单数据
        all_menus = await self.QueryWhere([SystemMenu.deleted == 0], fields=[SystemMenu.id, SystemMenu.parentId])
        
        # 构建父子关系映射
        parent_to_children = {}
        for menu in all_menus:
            if menu.parentId not in parent_to_children:
                parent_to_children[menu.parentId] = []
            parent_to_children[menu.parentId].append(menu.id)
        
        # 递归查找所有子菜单ID
        result = []
        
        def find_children(parent_ids):
            for parent_id in parent_ids:
                if parent_id in parent_to_children:
                    children = parent_to_children[parent_id]
                    result.extend(children)
                    find_children(children)
    
        find_children(menuIds)
        return result
    async def AddMenuShowBtn(self, menuId):
        entity = SystemMenu()
        entity.parentId = menuId
        entity.name = '展示菜单'
        entity.permission = '/'
        entity.type = 3
        entity.sort = 0
        entity.parentId = menuId
        entity.path = ''
        entity.icon = ''
        entity.component = ''
        entity.componentName = ''
        entity.status = 0
        entity.visible = 1
        entity.keepAlive = 1
        entity.alwaysShow = 1
        entity.deleted= 0
        await self.Insert(entity)
        return entity