import json
import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_tenant_package import SystemTenantPackage
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemTenantPackageDal(MyBaseDal[SystemTenantPackage]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemTenantPackage,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemTenantPackage],int]:
        fil = list()
        fil.append(SystemTenantPackage.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemTenantPackage,k) and v:
                fil.append(getattr(SystemTenantPackage,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemTenantPackage.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemTenantPackage.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemTenantPackage.DicType.ilike("%" + search_text + "%"),
            #                  SystemTenantPackage.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemTenantPackage.status == int(status))
        items, total_count = await self.paginate_query(fil, SystemTenantPackage.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemTenantPackage],int]:
        fil = list()
        fil.append(SystemTenantPackage.UID == self.UserId)
        fil.append(SystemTenantPackage.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemTenantPackage.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemTenantPackage.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemTenantPackage.status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemTenantPackage.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemTenantPackage]:
        fil = list()
        fil.append( SystemTenantPackage.deleted == 0)
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemTenantPackage.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemTenantPackage.status == int(status))
        items = await self.page_fields_nocount_query( SystemTenantPackage.get_mini_fields(), fil,  SystemTenantPackage.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemTenantPackage:
        entity = SystemTenantPackage()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemTenantPackage:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemTenantPackage=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        menuIds = jsonData.get('menuIds')
        if menuIds:
            entity.menuIds = json.dumps(menuIds)
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemTenantPackage.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemTenantPackage.id==id,SystemTenantPackage.UID==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemTenantPackage.id.in_(ids)])