import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_operate_log import SystemOperateLog
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemOperateLogDal(MyBaseDal[SystemOperateLog]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemOperateLog,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemOperateLog],int]:
        fil = list()
        fil.append(SystemOperateLog.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemOperateLog,k) and v:
                fil.append(getattr(SystemOperateLog,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemOperateLog.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemOperateLog.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemOperateLog.DicType.ilike("%" + search_text + "%"),
            #                  SystemOperateLog.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemOperateLog.Status == int(status))
        items, total_count = await self.paginate_query(fil, SystemOperateLog.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemOperateLog],int]:
        fil = list()
        fil.append(SystemOperateLog.userId == self.UserId)
        fil.append(SystemOperateLog.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemOperateLog.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemOperateLog.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemOperateLog.Status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemOperateLog.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemOperateLog]:
        fil = list()
        fil.append( SystemOperateLog.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemOperateLog,k) and v:
                fil.append(getattr(SystemOperateLog,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemOperateLog.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemOperateLog.Status == int(status))
        items = await self.page_fields_nocount_query( SystemOperateLog.get_mini_fields(), fil,  SystemOperateLog.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemOperateLog:
        entity = SystemOperateLog()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemOperateLog:
        entity = SystemOperateLog()
        entity.InitInsertEntityWithJson(jsonData)
        entity.userId=self.UserId
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemOperateLog:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemOperateLog=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemOperateLog:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemOperateLog=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemOperateLog.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemOperateLog.id==id,SystemOperateLog.userId==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemOperateLog.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemOperateLog.id.in_(ids),SystemOperateLog.userId==self.UserId])