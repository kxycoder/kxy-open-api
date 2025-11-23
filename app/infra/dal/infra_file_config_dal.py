import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.infra.models.infra_file_config import InfraFileConfig
from app.tools import utils

from app.common.basedal import MyBaseDal

class InfraFileConfigDal(MyBaseDal[InfraFileConfig]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(InfraFileConfig,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[InfraFileConfig],int]:
        fil = list()
        fil.append(InfraFileConfig.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraFileConfig,k) and v:
                fil.append(getattr(InfraFileConfig,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(InfraFileConfig.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(InfraFileConfig.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(InfraFileConfig.DicType.ilike("%" + search_text + "%"),
            #                  InfraFileConfig.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(InfraFileConfig.Status == int(status))
        items, total_count = await self.paginate_query(fil, InfraFileConfig.createTime.desc(), page_index, page_size)
        return items, total_count


    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[InfraFileConfig]:
        fil = list()
        fil.append( InfraFileConfig.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraFileConfig,k) and v:
                fil.append(getattr(InfraFileConfig,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( InfraFileConfig.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( InfraFileConfig.Status == int(status))
        items = await self.page_fields_nocount_query( InfraFileConfig.get_mini_fields(), fil,  InfraFileConfig.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->InfraFileConfig:
        entity = InfraFileConfig()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonData(self,jsonData)->InfraFileConfig:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:InfraFileConfig=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity



    async def Delete(self,id):
        await self.DeleteWhere([InfraFileConfig.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([InfraFileConfig.id.in_(ids)])

    async def GetMasterConfig(self)->InfraFileConfig:
        return await self.QueryOne([InfraFileConfig.master == 1, InfraFileConfig.deleted == 0])

    async def UpdateMaster(self,id):
        await self.UpdateFields([InfraFileConfig.master == 1],{'master':0})
        await self.UpdateFields([InfraFileConfig.id == id],{'master':1})
        
    async def GetBySotrageType(self,storage):
        return await self.QueryOne([InfraFileConfig.storage == storage, InfraFileConfig.deleted == 0])