import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_mail_template import SystemMailTemplate
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemMailTemplateDal(MyBaseDal[SystemMailTemplate]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemMailTemplate,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemMailTemplate],int]:
        fil = list()
        fil.append(SystemMailTemplate.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemMailTemplate,k) and v:
                fil.append(getattr(SystemMailTemplate,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemMailTemplate.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemMailTemplate.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemMailTemplate.DicType.ilike("%" + search_text + "%"),
            #                  SystemMailTemplate.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemMailTemplate.status == int(status))
        items, total_count = await self.paginate_query(fil, SystemMailTemplate.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemMailTemplate],int]:
        fil = list()
        fil.append(SystemMailTemplate.UID == self.UserId)
        fil.append(SystemMailTemplate.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemMailTemplate.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemMailTemplate.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemMailTemplate.status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemMailTemplate.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemMailTemplate]:
        fil = list()
        fil.append( SystemMailTemplate.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemMailTemplate,k) and v:
                fil.append(getattr(SystemMailTemplate,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemMailTemplate.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemMailTemplate.status == int(status))
        items = await self.page_fields_nocount_query( SystemMailTemplate.get_mini_fields(), fil,  SystemMailTemplate.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemMailTemplate:
        entity = SystemMailTemplate()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemMailTemplate:
        entity = SystemMailTemplate()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemMailTemplate:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemMailTemplate=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemMailTemplate:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemMailTemplate=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemMailTemplate.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemMailTemplate.id==id,SystemMailTemplate.UID==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemMailTemplate.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemMailTemplate.id.in_(ids),SystemMailTemplate.UID==self.UserId])