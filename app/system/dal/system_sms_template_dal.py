import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_sms_template import SystemSmsTemplate
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemSmsTemplateDal(MyBaseDal[SystemSmsTemplate]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemSmsTemplate,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemSmsTemplate],int]:
        fil = list()
        fil.append(SystemSmsTemplate.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemSmsTemplate,k) and v:
                fil.append(getattr(SystemSmsTemplate,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemSmsTemplate.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemSmsTemplate.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemSmsTemplate.DicType.ilike("%" + search_text + "%"),
            #                  SystemSmsTemplate.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemSmsTemplate.status == int(status))
        items, total_count = await self.paginate_query(fil, SystemSmsTemplate.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemSmsTemplate],int]:
        fil = list()
        fil.append(SystemSmsTemplate.UID == self.UserId)
        fil.append(SystemSmsTemplate.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemSmsTemplate.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemSmsTemplate.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemSmsTemplate.status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemSmsTemplate.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemSmsTemplate]:
        fil = list()
        fil.append( SystemSmsTemplate.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemSmsTemplate,k) and v:
                fil.append(getattr(SystemSmsTemplate,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemSmsTemplate.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemSmsTemplate.status == int(status))
        items = await self.page_fields_nocount_query( SystemSmsTemplate.get_mini_fields(), fil,  SystemSmsTemplate.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemSmsTemplate:
        entity = SystemSmsTemplate()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.params = utils.get_strings_params(entity.content)
        entity.status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemSmsTemplate:
        entity = SystemSmsTemplate()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemSmsTemplate:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemSmsTemplate=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemSmsTemplate:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemSmsTemplate=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemSmsTemplate.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemSmsTemplate.id==id,SystemSmsTemplate.UID==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemSmsTemplate.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemSmsTemplate.id.in_(ids),SystemSmsTemplate.UID==self.UserId])
    async def GetByCode(self,templateCode)->SystemSmsTemplate:
        return await self.QueryOne([SystemSmsTemplate.code==templateCode])