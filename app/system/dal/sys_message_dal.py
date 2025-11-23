import re
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.sys_message import SysMessage
from app.tools import utils

from app.common.basedal import BaseDal

class SysMessageDal(BaseDal[SysMessage]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SysMessage,session,**kwargs)
    
    # 获取列表
    async def Search(self,search,page_index, page_size)->tuple[List[SysMessage],int]:
        fil = list()
        fil.append(SysMessage.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SysMessage.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SysMessage.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SysMessage.DicType.ilike("%" + search_text + "%"),
            #                  SysMessage.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SysMessage.Status == int(status))
        items, total_count = await self.paginate_query(fil, SysMessage.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search,page_index, page_size)->tuple[List[SysMessage],int]:
        fil = list()
        fil.append(SysMessage.UID == str(self.UserId))
        msType = search.get('type')
        if msType:
            fil.append(SysMessage.MsgType == int(msType))
        # fil.append(SysMessage.IsRead == 0)
        fil.append(SysMessage.IsDelete == 0)
        items = await self.page_nocount_query(fil, SysMessage.CreateDate.desc(), page_index, page_size)
        return items, 0
    async def AddByJsonData(self, jsonData)->SysMessage:
        entity = SysMessage()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SysMessage:
        entity = SysMessage()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SysMessage:
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SysMessage=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SysMessage:
        '''更新客户自己的数据'''
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SysMessage=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.UpdateFields([SysMessage.Id==id],{'IsDelete':1})

    async def DeleteByUser(self,id):
        await self.UpdateFields([SysMessage.Id==id,SysMessage.UID==self.UserId],{'IsDelete':1})
    async def SendMsg(self,uid,msgType,title,content):
        msg = SysMessage()
        msg.UID= uid
        msg.MsgType = msgType
        msg.Title = title
        msg.Content = content
        msg.IsRead = 0
        msg.IsDelete = 0
        msg.Status = 1
        await self.Insert(msg)
        return msg
    async def UpdateBatch(self,messageIds:List[str]):
        await self.UpdateFields([SysMessage.Id.in_(messageIds),SysMessage.UID==self.UserId],{'IsRead':1})