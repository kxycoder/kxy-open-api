import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.filter import ignore_filter
from app.contract.types.user_vo import VoUserRole
from app.system.models.system_user_role import SystemUserRole
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemUserRoleDal(MyBaseDal[SystemUserRole]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemUserRole,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemUserRole],int]:
        fil = list()
        fil.append(SystemUserRole.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemUserRole,k) and v:
                fil.append(getattr(SystemUserRole,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemUserRole.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemUserRole.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemUserRole.DicType.ilike("%" + search_text + "%"),
            #                  SystemUserRole.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemUserRole.Status == int(status))
        items, total_count = await self.paginate_query(fil, SystemUserRole.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemUserRole],int]:
        fil = list()
        fil.append(SystemUserRole.userId == self.UserId)
        fil.append(SystemUserRole.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemUserRole.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemUserRole.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemUserRole.Status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemUserRole.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemUserRole]:
        fil = list()
        fil.append( SystemUserRole.deleted == 0)
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemUserRole.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemUserRole.Status == int(status))
        items = await self.page_fields_nocount_query( SystemUserRole.get_mini_fields(), fil,  SystemUserRole.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemUserRole:
        entity = SystemUserRole()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemUserRole:
        entity = SystemUserRole()
        entity.InitInsertEntityWithJson(jsonData)
        entity.userId=self.UserId
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemUserRole:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemUserRole=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemUserRole:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemUserRole=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemUserRole.id==id])

    async def DeleteByUser(self,userid):
        await self.DeleteWhere([SystemUserRole.userId==userid])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemUserRole.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemUserRole.id.in_(ids),SystemUserRole.userId==self.UserId])
    async def GetUserRoles(self,userid):
        return await self.QueryWhere([SystemUserRole.userId==userid,SystemUserRole.deleted==0])
    async def GetUserRoleIds(self,userid)->List[int]:
        roles= await self.QueryWhere([SystemUserRole.userId==userid,SystemUserRole.deleted==0],fields=[SystemUserRole.roleId])
        return [role.roleId for role in roles]
    @ignore_filter
    async def AssignUserRole(self,roles:VoUserRole,tenantId=None)->List[SystemUserRole]:
        if not tenantId:
            tenantId = self.CurrentTenantId
        await self.DeleteWhere([SystemUserRole.userId==roles.userId,SystemUserRole.tenantId==tenantId,SystemUserRole.deleted==0])
        items = []
        for roleId in roles.roleIds:
            item = SystemUserRole()
            item.userId = roles.userId
            item.roleId = roleId
            item.tenantId = tenantId
            items.append(item)
        await self.BatchInsert(items)
        return items
    @ignore_filter
    async def DeleteByTenantId(self,tenantId):
        await self.DeleteWhere([SystemUserRole.tenantId==tenantId])