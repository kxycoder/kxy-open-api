import re
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.sys_log import SysLog
from app.tools import utils
from app.common.basedal import BaseDal

class SysLogDal(BaseDal):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SysLog,session,**kwargs)
    
    # 获取列表
    async def Search(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        # fil.append(SysLog.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SysLog.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SysLog.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SysLog.DicType.ilike("%" + search_text + "%"),
            #                  SysLog.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SysLog.Status == int(status))
        items, total_count = await self.paginate_query(fil, SysLog.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        fil.append(SysLog.UID == self.UserId)
        fil.append(SysLog.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SysLog.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SysLog.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SysLog.Status == int(status))
        items, total_count = await self.paginate_query(fil, SysLog.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonData(self, jsonData)->SysLog:
        entity = SysLog()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SysLog:
        entity = SysLog()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SysLog:
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SysLog=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SysLog:
        '''更新客户自己的数据'''
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SysLog=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.UpdateFields([SysLog.Id==id],{'IsDelete':1})

    async def DeleteByUser(self,id):
        await self.UpdateFields([SysLog.Id==id,SysLog.UID==self.UserId],{'IsDelete':1})

    async def BatchAddLogs(self,logs:List[Dict[str,object]]):
        entities = []
        for log in logs:
            entity = SysLog()
            entity.InitInsertEntityWithJson(log)
            entities.append(entity)
        await self.BatchInsert(entities)