from datetime import datetime
import re
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.global_var import SendStatus
from app.system.models.message_send_setting import MessageSendSetting
from app.tools import utils

from app.common.basedal import BaseDal

class MessageSendSettingDal(BaseDal[MessageSendSetting]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(MessageSendSetting,session,**kwargs)
    
    # 获取列表
    async def Search(self,search,page_index, page_size)->tuple[List[MessageSendSetting],int]:
        fil = list()
        fil.append(MessageSendSetting.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MessageSendSetting.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MessageSendSetting.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(MessageSendSetting.DicType.ilike("%" + search_text + "%"),
            #                  MessageSendSetting.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(MessageSendSetting.Status == int(status))
        items, total_count = await self.paginate_query(fil, MessageSendSetting.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        fil.append(MessageSendSetting.UID == self.UserId)
        fil.append(MessageSendSetting.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MessageSendSetting.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MessageSendSetting.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(MessageSendSetting.Status == int(status))
        items, total_count = await self.paginate_query(fil, MessageSendSetting.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonData(self, jsonData)->MessageSendSetting:
        entity = MessageSendSetting()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->MessageSendSetting:
        entity = MessageSendSetting()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->MessageSendSetting:
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MessageSendSetting=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->MessageSendSetting:
        '''更新客户自己的数据'''
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MessageSendSetting=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.UpdateFields([MessageSendSetting.Id==id],{'IsDelete':1})

    async def DeleteByUser(self,id):
        await self.UpdateFields([MessageSendSetting.Id==id,MessageSendSetting.UID==self.UserId],{'IsDelete':1})
    async def GetBirthDaySetting(self,uid,friendId):
        return await self.QueryOne([MessageSendSetting.UID==uid,MessageSendSetting.EventName=="生日",MessageSendSetting.EventId==friendId])
    async def CloseBirthDayRemind(self,user_id,friendId):
        exist =await self.GetBirthDaySetting(user_id,friendId)
        if exist:
            exist.Status = SendStatus.Delete.value
            await self.Update(exist)
    async def CloseSendSetting(self,settingId):
        exist =await self.GetExistByUser(settingId)
        if exist:
            exist.Status = SendStatus.Delete.value
            exist.IsDelete = 1
            await self.Update(exist)
    async def CountUserSetting(self,uid)->int:
        return await self.QueryCount([MessageSendSetting.UID==uid,MessageSendSetting.IsDelete==0])
    async def GetNeedSendSettings(self,sendType,pageindex,pagesize=20)->List[MessageSendSetting]:
        # 1-创建 3-待发送 4-发送中 10-删除
        filter = [MessageSendSetting.SendType == sendType,MessageSendSetting.Status==SendStatus.Wait.value,MessageSendSetting.IsDelete==0,MessageSendSetting.NextSendTime<=datetime.now()]
        return await self.page_nocount_query(filter,MessageSendSetting.Id.asc(),pageindex,pagesize)
    async def GetByEvent(self,eventId,eventName):
        return await self.QueryOne([MessageSendSetting.UID==self.UserId, MessageSendSetting.EventId==eventId,MessageSendSetting.EventName==eventName])
    async def GetByEventActive(self,eventId,eventName):
        return await self.QueryOne([MessageSendSetting.UID==self.UserId, MessageSendSetting.EventId==eventId,MessageSendSetting.EventName==eventName,MessageSendSetting.IsDelete==0])
    async def GetByEvents(self,eventId,eventName):
        return await self.QueryWhere([MessageSendSetting.EventId==eventId,MessageSendSetting.EventName==eventName,MessageSendSetting.IsDelete==0])
    
    async def DeleteFriendId(self,friendId):
        return await self.Delete([MessageSendSetting.EventName=='生日', MessageSendSetting.EventId==friendId])
    async def GetByEventIds(self,eventIds,eventName)->List[MessageSendSetting]:
        return await self.QueryWhere([MessageSendSetting.EventName==eventName,MessageSendSetting.EventId.in_(eventIds),MessageSendSetting.IsDelete==0])