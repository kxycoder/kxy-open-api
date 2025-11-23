from datetime import datetime
import re
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.message_send_record import MessageSendRecord
from app.system.models.message_send_setting import MessageSendSetting
from app.tools import utils

from app.common.basedal import BaseDal

class MessageSendRecordDal(BaseDal[MessageSendRecord]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(MessageSendRecord,session,**kwargs)
    
    # 获取列表
    async def Search(self,search,page_index, page_size)->tuple[List[MessageSendRecord],int]:
        fil = list()
        fil.append(MessageSendRecord.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MessageSendRecord.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MessageSendRecord.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(MessageSendRecord.DicType.ilike("%" + search_text + "%"),
            #                  MessageSendRecord.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(MessageSendRecord.Status == int(status))
        items, total_count = await self.paginate_query(fil, MessageSendRecord.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        fil.append(MessageSendRecord.UID == self.UserId)
        fil.append(MessageSendRecord.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MessageSendRecord.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MessageSendRecord.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(MessageSendRecord.Status == int(status))
        items, total_count = await self.paginate_query(fil, MessageSendRecord.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonData(self, jsonData)->MessageSendRecord:
        entity = MessageSendRecord()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->MessageSendRecord:
        entity = MessageSendRecord()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->MessageSendRecord:
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MessageSendRecord=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->MessageSendRecord:
        '''更新客户自己的数据'''
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MessageSendRecord=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.UpdateFields([MessageSendRecord.Id==id],{'IsDelete':1})

    async def DeleteByUser(self,id):
        await self.UpdateFields([MessageSendRecord.Id==id,MessageSendRecord.UID==self.UserId],{'IsDelete':1})
    async def AddSendRecord(self,phone,requestId,setting:MessageSendSetting,status,msg=''):
        entity = MessageSendRecord()
        entity.RequestId=requestId
        entity.MsgSettingId=setting.Id
        entity.SendType=setting.SendType
        entity.SendContent=setting.SendContent
        entity.SendTemplateCode=setting.SendTemplateCode
        entity.SendTemplateParam=setting.SendTemplateParam
        entity.EventName=setting.EventName
        entity.SendTime = datetime.now()
        entity.Phone = phone
        entity.Status = status
        entity.Remark = msg[:200]
        await self.Insert(entity)
        return entity
    async def GetExistByRequestId(self,requestId):
        return await self.QueryOne([MessageSendRecord.RequestId==requestId])
    async def UpdateByRequestId(self,requestId,send_time,success:bool,msg:str):
        """根据请求ID更新记录"""
        if not requestId:
            raise FriendlyException('更新时必须传回请求ID')
        entity:MessageSendRecord = await self.GetExistByRequestId(requestId)
        if not entity:
            return f'未找到请求ID为{requestId}的记录'
        entity.Status = 5 if success else 10
        entity.SendTime = send_time
        entity.Remark = msg[:100]
        await self.Update(entity)
        return entity