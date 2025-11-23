import json
import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.filter import ignore_filter
from app.system.models.system_role import SystemRole
from app.tools import utils
from kxy.framework.context import kxy_roles

from app.common.basedal import MyBaseDal

class SystemRoleDal(MyBaseDal[SystemRole]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemRole,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemRole],int]:
        fil = list()
        fil.append(SystemRole.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemRole,k) and v:
                fil.append(getattr(SystemRole,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemRole.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemRole.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemRole.DicType.ilike("%" + search_text + "%"),
            #                  SystemRole.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemRole.status == int(status))
        items, total_count = await self.paginate_query(fil, SystemRole.sort.asc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemRole],int]:
        fil = list()
        fil.append(SystemRole.UID == self.UserId)
        fil.append(SystemRole.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemRole.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemRole.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemRole.status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemRole.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemRole]:
        fil = list()
        fil.append(SystemRole.deleted == 0)
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemRole.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemRole.status == int(status))
        items = await self.page_fields_nocount_query( SystemRole.get_mini_fields(), fil,  SystemRole.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemRole:
        entity = SystemRole()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.status = 0
        entity.deleted = 0
        # 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）
        entity.dataScope = 2
        entity.dataScopeDeptIds = []
        entity.type =2
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemRole:
        entity = SystemRole()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemRole:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemRole=await self.GetExist(id)
        if entity.type==1 and 'super_admin' not in kxy_roles.get():
            raise FriendlyException('系统内置角色不允许修改')
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemRole:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemRole=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemRole.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemRole.id==id,SystemRole.UID==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemRole.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemRole.id.in_(ids),SystemRole.UID==self.UserId])
    async def assign_role_data_scope(self,roleId,dataScope,dataScopeDeptIds):
        exist  = await self.GetExist(roleId)
        exist.dataScope = dataScope
        exist.dataScopeDeptIds = dataScopeDeptIds
        await self.Update(exist)
        return exist
    async def GetRoleNameByIds(self,roleIds)->List[str]:
        roles =  await self.QueryWhere([SystemRole.id.in_(roleIds),SystemRole.deleted==0],fields=[SystemRole.code])
        return [role.code for role in roles]
    async def GetRolesByIds(self,roleIds)->List[SystemRole]:
        roles =  await self.QueryWhere([SystemRole.id.in_(roleIds),SystemRole.deleted==0],fields=[SystemRole.id,SystemRole.code,SystemRole.name])
        return roles
    async def GetAllTenantRoles(self)->List[int]:
        roleIds = await self.QueryWhere([SystemRole.deleted==0],fields=[SystemRole.id])
        return [role.id for role in roleIds]
        
    @ignore_filter
    async def InitTenantAdminRole(self,tenantId):
        entity = SystemRole()
        entity.name='管理员'
        entity.code='admin'
        entity.type=1
        entity.dataScope = 1
        entity.dataScopeDeptIds = []
        entity.status = 0
        entity.tenantId = tenantId
        entity.deleted = 0
        await self.Insert(entity)
        return entity
    @ignore_filter
    async def DeleteByTenantId(self,tenantId):
        await self.DeleteWhere([SystemRole.tenantId==tenantId])

    @ignore_filter
    async def GetAdminRolesByTenantIds(self,tenantIds)->List[SystemRole]:
        return await self.QueryWhere([SystemRole.tenantId.in_(tenantIds),SystemRole.code=='admin',SystemRole.type==1,SystemRole.deleted==0],fields=[SystemRole.id,SystemRole.tenantId])