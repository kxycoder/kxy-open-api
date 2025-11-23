import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_notify_template import SystemNotifyTemplate
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemNotifyTemplateDal(MyBaseDal[SystemNotifyTemplate]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemNotifyTemplate,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemNotifyTemplate],int]:
        fil = list()
        fil.append(SystemNotifyTemplate.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemNotifyTemplate,k) and v:
                fil.append(getattr(SystemNotifyTemplate,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemNotifyTemplate.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemNotifyTemplate.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemNotifyTemplate.DicType.ilike("%" + search_text + "%"),
            #                  SystemNotifyTemplate.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemNotifyTemplate.status == int(status))
        items, total_count = await self.paginate_query(fil, SystemNotifyTemplate.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemNotifyTemplate],int]:
        fil = list()
        fil.append(SystemNotifyTemplate.UID == self.UserId)
        fil.append(SystemNotifyTemplate.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemNotifyTemplate.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemNotifyTemplate.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemNotifyTemplate.status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemNotifyTemplate.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemNotifyTemplate]:
        fil = list()
        fil.append( SystemNotifyTemplate.deleted == 0)
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemNotifyTemplate.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemNotifyTemplate.status == int(status))
        items = await self.page_fields_nocount_query( SystemNotifyTemplate.get_mini_fields(), fil,  SystemNotifyTemplate.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemNotifyTemplate:
        entity = SystemNotifyTemplate()
        entity.InitInsertEntityWithJson(jsonData)
        params = utils.get_strings_params(entity.content) 
        entity.params = params
        entity.status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemNotifyTemplate:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemNotifyTemplate=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        params = utils.get_strings_params(entity.content) 
        entity.params = params
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemNotifyTemplate.id==id])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemNotifyTemplate.id.in_(ids)])
    async def GetByCode(self,templateCode)->SystemNotifyTemplate:
        return await self.QueryOne([SystemNotifyTemplate.code==templateCode])