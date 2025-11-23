import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.infra.models.infra_config import InfraConfig
from app.tools import utils

from app.common.basedal import MyBaseDal

class InfraConfigDal(MyBaseDal[InfraConfig]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(InfraConfig,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[InfraConfig],int]:
        fil = list()
        fil.append(InfraConfig.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraConfig,k) and v:
                fil.append(getattr(InfraConfig,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(InfraConfig.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(InfraConfig.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(InfraConfig.DicType.ilike("%" + search_text + "%"),
            #                  InfraConfig.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(InfraConfig.Status == int(status))
        items, total_count = await self.paginate_query(fil, InfraConfig.createTime.desc(), page_index, page_size)
        return items, total_count


    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[InfraConfig]:
        fil = list()
        fil.append( InfraConfig.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraConfig,k) and v:
                fil.append(getattr(InfraConfig,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( InfraConfig.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( InfraConfig.Status == int(status))
        items = await self.page_fields_nocount_query( InfraConfig.get_mini_fields(), fil,  InfraConfig.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->InfraConfig:
        entity = InfraConfig()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity
    async def UpdateByJsonData(self,jsonData)->InfraConfig:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:InfraConfig=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([InfraConfig.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([InfraConfig.id.in_(ids)])

    async def GetByKey(self,key:str)->str:
        exist =  await self.QueryOne([InfraConfig.key==key,InfraConfig.deleted==0])
        if exist:
            return exist.value
        return ''