import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_login_log import SystemLoginLog
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemLoginLogDal(MyBaseDal[SystemLoginLog]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemLoginLog,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemLoginLog],int]:
        fil = list()
        fil.append(SystemLoginLog.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemLoginLog,k) and v:
                fil.append(getattr(SystemLoginLog,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemLoginLog.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemLoginLog.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemLoginLog.DicType.ilike("%" + search_text + "%"),
            #                  SystemLoginLog.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemLoginLog.Status == int(status))
        items, total_count = await self.paginate_query(fil, SystemLoginLog.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemLoginLog],int]:
        fil = list()
        fil.append(SystemLoginLog.userId == self.UserId)
        fil.append(SystemLoginLog.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemLoginLog.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemLoginLog.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemLoginLog.Status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemLoginLog.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemLoginLog]:
        fil = list()
        fil.append( SystemLoginLog.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemLoginLog,k) and v:
                fil.append(getattr(SystemLoginLog,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemLoginLog.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemLoginLog.Status == int(status))
        items = await self.page_fields_nocount_query( SystemLoginLog.get_mini_fields(), fil,  SystemLoginLog.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemLoginLog:
        entity = SystemLoginLog()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemLoginLog:
        entity = SystemLoginLog()
        entity.InitInsertEntityWithJson(jsonData)
        entity.userId=self.UserId
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemLoginLog:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemLoginLog=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemLoginLog:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemLoginLog=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemLoginLog.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemLoginLog.id==id,SystemLoginLog.userId==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemLoginLog.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemLoginLog.id.in_(ids),SystemLoginLog.userId==self.UserId])