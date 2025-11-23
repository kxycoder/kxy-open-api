import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.infra.models.infra_job import InfraJob
from app.tools import utils

from app.common.basedal import MyBaseDal

class InfraJobDal(MyBaseDal[InfraJob]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(InfraJob,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[InfraJob],int]:
        fil = list()
        fil.append(InfraJob.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraJob,k) and v:
                fil.append(getattr(InfraJob,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(InfraJob.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(InfraJob.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(InfraJob.DicType.ilike("%" + search_text + "%"),
            #                  InfraJob.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(InfraJob.status == int(status))
        items, total_count = await self.paginate_query(fil, InfraJob.createTime.desc(), page_index, page_size)
        return items, total_count


    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[InfraJob]:
        fil = list()
        fil.append( InfraJob.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraJob,k) and v:
                fil.append(getattr(InfraJob,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( InfraJob.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( InfraJob.status == int(status))
        items = await self.page_fields_nocount_query( InfraJob.get_mini_fields(), fil,  InfraJob.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->InfraJob:
        entity = InfraJob()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonData(self,jsonData)->InfraJob:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:InfraJob=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity



    async def Delete(self,id):
        await self.DeleteWhere([InfraJob.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([InfraJob.id.in_(ids)])

