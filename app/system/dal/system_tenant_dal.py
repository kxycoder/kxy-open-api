from datetime import datetime
import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.contract.types.user_vo import VoUserTenant
from app.system.models.system_tenant import SystemTenant
from app.tools import utils
from kxy.framework.date_util import DateUtil

from app.common.basedal import MyBaseDal

class SystemTenantDal(MyBaseDal[SystemTenant]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemTenant,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemTenant],int]:
        fil = list()
        fil.append(SystemTenant.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemTenant,k) and v:
                fil.append(getattr(SystemTenant,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemTenant.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemTenant.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemTenant.DicType.ilike("%" + search_text + "%"),
            #                  SystemTenant.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemTenant.status == int(status))
        items, total_count = await self.paginate_query(fil, SystemTenant.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemTenant],int]:
        fil = list()
        fil.append(SystemTenant.UID == self.UserId)
        fil.append(SystemTenant.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemTenant.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemTenant.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemTenant.status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemTenant.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemTenant]:
        fil = list()
        fil.append( SystemTenant.deleted == 0)
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemTenant.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemTenant.status == int(status))
        items = await self.page_fields_nocount_query( SystemTenant.get_mini_fields(), fil,  SystemTenant.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemTenant:
        entity = SystemTenant()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemTenant:
        entity = SystemTenant()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemTenant:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemTenant=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemTenant:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemTenant=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemTenant.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemTenant.id==id,SystemTenant.UID==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemTenant.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemTenant.id.in_(ids),SystemTenant.UID==self.UserId])
    async def AddTenant(self,tenant:VoUserTenant):
        entity = SystemTenant()
        entity.name=tenant.name
        entity.contactName=tenant.contactName
        entity.contactMobile=tenant.contactMobile
        entity.website=tenant.website
        entity.status=tenant.status
        entity.packageId=tenant.packageId
        entity.expireTime=utils.convert_timestamp_to_datetime(tenant.expireTime)
        entity.accountCount = tenant.accountCount
        entity.accountCount=tenant.accountCount
        entity.deleted = 0
        entity.status = 0
        await self.Insert(entity)
        return entity
    async def GetByPackageId(self,packageId)->List[SystemTenant]:
        return await self.QueryWhere([SystemTenant.packageId==packageId,SystemTenant.deleted==0])
    async def GetIdByName(self,name)->SystemTenant:
        return await self.QueryOne([SystemTenant.name==name,SystemTenant.deleted==0])