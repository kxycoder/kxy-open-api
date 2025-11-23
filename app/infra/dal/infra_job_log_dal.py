import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.infra.models.infra_job_log import InfraJobLog
from app.tools import utils

from app.common.basedal import MyBaseDal

class InfraJobLogDal(MyBaseDal[InfraJobLog]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(InfraJobLog,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[InfraJobLog],int]:
        fil = list()
        fil.append(InfraJobLog.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraJobLog,k) and v:
                fil.append(getattr(InfraJobLog,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(InfraJobLog.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(InfraJobLog.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(InfraJobLog.DicType.ilike("%" + search_text + "%"),
            #                  InfraJobLog.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(InfraJobLog.status == int(status))
        items, total_count = await self.paginate_query(fil, InfraJobLog.createTime.desc(), page_index, page_size)
        return items, total_count
    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[InfraJobLog]:
        fil = list()
        fil.append( InfraJobLog.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraJobLog,k) and v:
                fil.append(getattr(InfraJobLog,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( InfraJobLog.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( InfraJobLog.status == int(status))
        items = await self.page_fields_nocount_query( InfraJobLog.get_mini_fields(), fil,  InfraJobLog.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->InfraJobLog:
        entity = InfraJobLog()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity
    async def UpdateByJsonData(self,jsonData)->InfraJobLog:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:InfraJobLog=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([InfraJobLog.id==id])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([InfraJobLog.id.in_(ids)])
