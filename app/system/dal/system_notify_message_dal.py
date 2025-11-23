import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_notify_message import SystemNotifyMessage
from app.system.models.system_notify_template import SystemNotifyTemplate
from app.tools import utils
from kxy.framework.filter import ignore_filter

from app.common.basedal import MyBaseDal

class SystemNotifyMessageDal(MyBaseDal[SystemNotifyMessage]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemNotifyMessage,session,**kwargs)
    
    @ignore_filter
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemNotifyMessage],int]:
        fil = list()
        fil.append(SystemNotifyMessage.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemNotifyMessage,k) and v:
                fil.append(getattr(SystemNotifyMessage,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemNotifyMessage.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemNotifyMessage.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemNotifyMessage.DicType.ilike("%" + search_text + "%"),
            #                  SystemNotifyMessage.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemNotifyMessage.readStatus == status)
        items, total_count = await self.paginate_query(fil, SystemNotifyMessage.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemNotifyMessage],int]:
        fil = list()
        fil.append(SystemNotifyMessage.userId == self.UserId)
        fil.append(SystemNotifyMessage.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemNotifyMessage.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemNotifyMessage.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemNotifyMessage.Status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemNotifyMessage.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemNotifyMessage]:
        fil = list()
        fil.append( SystemNotifyMessage.deleted == 0)
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemNotifyMessage.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemNotifyMessage.Status == int(status))
        items = await self.page_fields_nocount_query( SystemNotifyMessage.get_mini_fields(), fil,  SystemNotifyMessage.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemNotifyMessage:
        entity = SystemNotifyMessage()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemNotifyMessage:
        entity = SystemNotifyMessage()
        entity.InitInsertEntityWithJson(jsonData)
        entity.userId=self.UserId
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemNotifyMessage:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemNotifyMessage=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemNotifyMessage:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemNotifyMessage=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemNotifyMessage.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemNotifyMessage.id==id,SystemNotifyMessage.userId==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemNotifyMessage.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemNotifyMessage.id.in_(ids),SystemNotifyMessage.userId==self.UserId])
    async def GetUnreadCount(self):
        return await self.QueryCount([SystemNotifyMessage.readStatus=='0',SystemNotifyMessage.deleted == 0])
    
    async def SendMessage(self,notice):
        pass
    async def GetUnreadList(self):
        return await self.QueryWhere([SystemNotifyMessage.readStatus=='0',SystemNotifyMessage.deleted == 0])