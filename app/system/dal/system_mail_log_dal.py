import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_mail_log import SystemMailLog
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemMailLogDal(MyBaseDal[SystemMailLog]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemMailLog,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemMailLog],int]:
        fil = list()
        fil.append(SystemMailLog.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemMailLog,k) and v:
                fil.append(getattr(SystemMailLog,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemMailLog.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemMailLog.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemMailLog.DicType.ilike("%" + search_text + "%"),
            #                  SystemMailLog.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemMailLog.Status == int(status))
        items, total_count = await self.paginate_query(fil, SystemMailLog.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemMailLog],int]:
        fil = list()
        fil.append(SystemMailLog.userId == self.UserId)
        fil.append(SystemMailLog.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemMailLog.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemMailLog.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemMailLog.Status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemMailLog.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemMailLog]:
        fil = list()
        fil.append( SystemMailLog.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemMailLog,k) and v:
                fil.append(getattr(SystemMailLog,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemMailLog.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemMailLog.Status == int(status))
        items = await self.page_fields_nocount_query( SystemMailLog.get_mini_fields(), fil,  SystemMailLog.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemMailLog:
        entity = SystemMailLog()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemMailLog:
        entity = SystemMailLog()
        entity.InitInsertEntityWithJson(jsonData)
        entity.userId=self.UserId
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemMailLog:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemMailLog=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemMailLog:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemMailLog=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemMailLog.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemMailLog.id==id,SystemMailLog.userId==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemMailLog.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemMailLog.id.in_(ids),SystemMailLog.userId==self.UserId])