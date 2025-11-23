import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.filter import ignore_filter
from app.system.models.system_role_menu import SystemRoleMenu
from app.tools import utils
from kxy.framework.delete_safe_list import DeleteSafeList

from app.common.basedal import MyBaseDal

class SystemRoleMenuDal(MyBaseDal[SystemRoleMenu]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemRoleMenu,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemRoleMenu],int]:
        fil = list()
        fil.append(SystemRoleMenu.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemRoleMenu,k) and v:
                fil.append(getattr(SystemRoleMenu,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemRoleMenu.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemRoleMenu.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemRoleMenu.DicType.ilike("%" + search_text + "%"),
            #                  SystemRoleMenu.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemRoleMenu.Status == int(status))
        items, total_count = await self.paginate_query(fil, SystemRoleMenu.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemRoleMenu],int]:
        fil = list()
        fil.append(SystemRoleMenu.UID == self.UserId)
        fil.append(SystemRoleMenu.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemRoleMenu.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemRoleMenu.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemRoleMenu.Status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemRoleMenu.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemRoleMenu]:
        fil = list()
        fil.append( SystemRoleMenu.deleted == 0)
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemRoleMenu.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemRoleMenu.Status == int(status))
        items = await self.page_fields_nocount_query( SystemRoleMenu.get_mini_fields(), fil,  SystemRoleMenu.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemRoleMenu:
        entity = SystemRoleMenu()
        entity.InitInsertEntityWithJson(jsonData)
        entity.tenantId = self.CurrentTenantId
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemRoleMenu:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemRoleMenu=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemRoleMenu:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemRoleMenu=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemRoleMenu.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemRoleMenu.id==id,SystemRoleMenu.UID==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemRoleMenu.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemRoleMenu.id.in_(ids),SystemRoleMenu.UID==self.UserId])
    
    async def ListRoleMenus(self,roleId,tenantId=0)->List[int]:
        if not tenantId:
            tenantId = self.CurrentTenantId
        data= await self.QueryWhere([SystemRoleMenu.roleId==roleId,SystemRoleMenu.deleted==0,SystemRoleMenu.tenantId==tenantId],fields=[SystemRoleMenu.menuId])
        return [x.menuId for x in data]
    async def DeleteBatchByRoleId(self,roleId,tenantId=0):
        if not tenantId:
            tenantId = self.CurrentTenantId
        return await self.DeleteWhere([SystemRoleMenu.roleId==roleId,SystemRoleMenu.tenantId==tenantId, SystemRoleMenu.deleted==0])
    async def AssignRoleMenus(self,roleId:int,menuIds:List[int],tenantId=0):
        if not tenantId:
            tenantId = self.CurrentTenantId
        existMenuIds = await self.ListRoleMenus(roleId,tenantId)
        needDelete,newIds=DeleteSafeList(existMenuIds).diffrent_with(menuIds)
        items = []
        for menuId in newIds:
            entity = SystemRoleMenu()
            entity.roleId = roleId
            entity.menuId = menuId
            entity.tenantId = tenantId
            items.append(entity)
        if items:
            await self.BatchInsert(items)
        await self.DeleteWhere([SystemRoleMenu.roleId==roleId,SystemRoleMenu.menuId.in_(needDelete), SystemRoleMenu.tenantId==tenantId])
    
    async def GetRolesMenuId(self,userRoleIds:List[int],tenantId=0)->List[int]:
        fil = []
        if userRoleIds:
            fil.append(SystemRoleMenu.roleId.in_(userRoleIds))
        if not tenantId:
            tenantId = self.CurrentTenantId
        fil.append(SystemRoleMenu.deleted==0)
        rows = await self.QueryWhere(fil)
        return [row.menuId for row in rows]
    
    async def DeleteByTenantId(self,tenantId):
        await self.DeleteWhere([SystemRoleMenu.tenantId==tenantId])