import re
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.sys_user_extend import SysUserExtend
from app.tools import utils

from app.common.basedal import BaseDal

class SysUserExtendDal(BaseDal[SysUserExtend]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SysUserExtend,session,**kwargs)
    
    # 获取列表
    async def Search(self,search,page_index, page_size)->tuple[List[SysUserExtend],int]:
        fil = list()
        fil.append(SysUserExtend.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SysUserExtend.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SysUserExtend.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SysUserExtend.DicType.ilike("%" + search_text + "%"),
            #                  SysUserExtend.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SysUserExtend.Status == int(status))
        items, total_count = await self.paginate_query(fil, SysUserExtend.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search,page_index, page_size, need_count=True)->tuple[Sequence,int]:
        fil = list()
        fil.append(SysUserExtend.UID == self.UserId)
        fil.append(SysUserExtend.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SysUserExtend.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SysUserExtend.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SysUserExtend.Status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SysUserExtend.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonData(self, jsonData)->SysUserExtend:
        entity = SysUserExtend()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SysUserExtend:
        entity = SysUserExtend()
        entity.InitInsertEntityWithJson(jsonData)
        # entity.UID=self.UserId
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SysUserExtend:
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SysUserExtend=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SysUserExtend:
        '''更新客户自己的数据'''
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SysUserExtend=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        # entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.UpdateFields([SysUserExtend.Id==id],{'IsDelete':1})

    async def DeleteByUser(self,id):
        await self.UpdateFields([SysUserExtend.Id==id,SysUserExtend.UID==self.UserId],{'IsDelete':1})
    async def InitUser(self,userId,count=0):
        entity = SysUserExtend()
        entity.Id = userId
        entity.Count = 5 + count
        entity.UnReadMsg = 0
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity
    async def UpdateCount(self,sourceUser,count):
        exist = await self.Get(sourceUser)
        if not exist:
            entity = await self.InitUser(sourceUser,count)
            return entity
        else:
            if count<0 and exist.Count<=0:
                raise FriendlyException('提醒次数不足')  
            exist.Count = count + exist.Count
            await self.Update(exist)
            return exist
    async def GetCount(self,uid)->int:
        result = await self.QueryOne([SysUserExtend.Id==uid],fields=[SysUserExtend.Count])
        if not result:
            entity = await self.InitUser(uid)
            return entity.Count
        return result.Count
    # 减少次数
    async def ReduceCount(self,uid):
        await self.UpdateCount(uid, - 1)
    # 增加次数
    async def AddCount(self,uid):
        await self.UpdateCount(uid, 1)
    async def AddUnRead(self,uid):
        exist = await self.Get(uid)
        if not exist.UnReadMsg:
            exist.UnReadMsg = 1
        else:
            exist.UnReadMsg = exist.UnReadMsg + 1
        await self.UpdateFields([SysUserExtend.Id==uid],{'UnReadMsg':exist.UnReadMsg})
    async def ReduceUnRead(self,uid,count=1):
        exist = await self.Get(uid)
        if not exist.UnReadMsg:
            exist.UnReadMsg = 0
        else:
            if exist.UnReadMsg>=count:
                exist.UnReadMsg = exist.UnReadMsg - count
            else:
                exist.UnReadMsg = 0
        await self.UpdateFields([SysUserExtend.Id==uid],{'UnReadMsg':exist.UnReadMsg})
        
    async def GetUserExtend(self,uid):
        exist =await self.QueryOne([SysUserExtend.Id==uid],fields=[SysUserExtend.Count,SysUserExtend.UnReadMsg])
        if not exist:
            return await self.InitUser(uid)
        return exist