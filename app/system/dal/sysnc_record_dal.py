# coding=UTF-8

from app.common.basedal import BaseDal
from kxy.framework.friendly_exception import FriendlyException
from sqlalchemy.ext.asyncio import AsyncSession
from app.system.models.sysnc_record import SysncRecord
from datetime import datetime
import re

class SysncRecordDal(BaseDal[SysncRecord]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__(SysncRecord,db,**kwargs)

    # 获取列表
    async def List(self,search, page_index, page_size):
        fil = list()

        fil.append(SysncRecord.Status != 10)
        #if search:
        #    if re.search(r"^(\d)*$", search):
        #        fil.append(SysncRecord.ID == int(search))
        #    else:
        #        search =search.strip()
        #        fil.append(SysncRecord.Name.ilike("%" + search + "%"))
        return await self.paginate_query(fil, SysncRecord.CreateDate.desc(), page_index, page_size)
    # 创建

    async def AddByJsonData(self, jsonData):
        entity = SysncRecord()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        await self.Insert(entity)
        return entity
    async def Delete(self,id):
        exist=await self.Get(id)
        if exist!=None:
            exist.Status=10
            await self.Update(exist)
        else:
            raise FriendlyException('不存在'+str(id)+'的数据')
    async def UpdateByJsonData(self,jsonData):
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity=await self.Get(id)
        if not entity:
            raise FriendlyException('不存在'+str(id)+"的数据")
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity
    async def AddByField(self, synctype,SystemCode):
        entity=SysncRecord()
        entity.SyncType=synctype
        entity.SystemCode=SystemCode
        entity.SyncDate=datetime.now()
        entity.Status=1
        await self.Insert(entity)
        return entity

    async def GetLastSyncDate(self,synctype,SystemCode):
        return await self.QueryOne([SysncRecord.SyncType==synctype,SysncRecord.Status==5,SysncRecord.SystemCode==SystemCode],orderBy=[SysncRecord.SyncDate.desc()])
    async def CreateSyncRecord(self,synctype,SystemCode):        
        return await self.AddByField(synctype,SystemCode)
    async def SetSucces(self,id):
        exist=await self.Get(id)
        exist.Status=5
        await self.Update(exist)