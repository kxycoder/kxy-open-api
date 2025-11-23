import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.infra.models.infra_template import InfraTemplate
from app.tools import utils

from app.common.basedal import MyBaseDal

class InfraTemplateDal(MyBaseDal[InfraTemplate]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(InfraTemplate,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[InfraTemplate],int]:
        fil = list()
        fil.append(InfraTemplate.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraTemplate,k) and v:
                fil.append(getattr(InfraTemplate,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(InfraTemplate.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(InfraTemplate.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(InfraTemplate.DicType.ilike("%" + search_text + "%"),
            #                  InfraTemplate.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(InfraTemplate.Status == int(status))
        items, total_count = await self.paginate_query(fil, InfraTemplate.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[InfraTemplate]:
        fil = list()
        fil.append( InfraTemplate.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraTemplate,k) and v:
                fil.append(getattr(InfraTemplate,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( InfraTemplate.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( InfraTemplate.Status == int(status))
        items = await self.page_fields_nocount_query( InfraTemplate.get_mini_fields(), fil,  InfraTemplate.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->InfraTemplate:
        entity = InfraTemplate()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonData(self,jsonData)->InfraTemplate:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:InfraTemplate=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([InfraTemplate.id==id])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([InfraTemplate.id.in_(ids)])
    async def GetTempaltes(self)->List[InfraTemplate]:
        return await self.QueryWhere([InfraTemplate.deleted==0],fields=[InfraTemplate.id,InfraTemplate.name,InfraTemplate.variable])