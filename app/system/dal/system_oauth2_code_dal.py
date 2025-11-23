import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_oauth2_code import SystemOauth2Code
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemOauth2CodeDal(MyBaseDal[SystemOauth2Code]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemOauth2Code,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemOauth2Code],int]:
        fil = list()
        fil.append(SystemOauth2Code.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemOauth2Code,k) and v:
                fil.append(getattr(SystemOauth2Code,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemOauth2Code.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemOauth2Code.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemOauth2Code.DicType.ilike("%" + search_text + "%"),
            #                  SystemOauth2Code.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemOauth2Code.Status == int(status))
        items, total_count = await self.paginate_query(fil, SystemOauth2Code.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemOauth2Code],int]:
        fil = list()
        fil.append(SystemOauth2Code.userId == self.UserId)
        fil.append(SystemOauth2Code.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemOauth2Code.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemOauth2Code.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemOauth2Code.Status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemOauth2Code.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemOauth2Code]:
        fil = list()
        fil.append( SystemOauth2Code.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemOauth2Code,k) and v:
                fil.append(getattr(SystemOauth2Code,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemOauth2Code.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemOauth2Code.Status == int(status))
        items = await self.page_fields_nocount_query( SystemOauth2Code.get_mini_fields(), fil,  SystemOauth2Code.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemOauth2Code:
        entity = SystemOauth2Code()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemOauth2Code:
        entity = SystemOauth2Code()
        entity.InitInsertEntityWithJson(jsonData)
        entity.userId=self.UserId
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemOauth2Code:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemOauth2Code=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemOauth2Code:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemOauth2Code=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemOauth2Code.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemOauth2Code.id==id,SystemOauth2Code.userId==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemOauth2Code.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemOauth2Code.id.in_(ids),SystemOauth2Code.userId==self.UserId])