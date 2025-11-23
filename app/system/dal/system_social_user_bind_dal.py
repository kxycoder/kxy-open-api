import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_social_user_bind import SystemSocialUserBind
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemSocialUserBindDal(MyBaseDal[SystemSocialUserBind]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemSocialUserBind,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemSocialUserBind],int]:
        fil = list()
        fil.append(SystemSocialUserBind.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemSocialUserBind,k) and v:
                fil.append(getattr(SystemSocialUserBind,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemSocialUserBind.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemSocialUserBind.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemSocialUserBind.DicType.ilike("%" + search_text + "%"),
            #                  SystemSocialUserBind.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemSocialUserBind.Status == int(status))
        items, total_count = await self.paginate_query(fil, SystemSocialUserBind.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemSocialUserBind],int]:
        fil = list()
        fil.append(SystemSocialUserBind.userId == self.UserId)
        fil.append(SystemSocialUserBind.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemSocialUserBind.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemSocialUserBind.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemSocialUserBind.Status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemSocialUserBind.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemSocialUserBind]:
        fil = list()
        fil.append( SystemSocialUserBind.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemSocialUserBind,k) and v:
                fil.append(getattr(SystemSocialUserBind,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemSocialUserBind.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemSocialUserBind.Status == int(status))
        items = await self.page_fields_nocount_query( SystemSocialUserBind.get_mini_fields(), fil,  SystemSocialUserBind.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemSocialUserBind:
        entity = SystemSocialUserBind()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemSocialUserBind:
        entity = SystemSocialUserBind()
        entity.InitInsertEntityWithJson(jsonData)
        entity.userId=self.UserId
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemSocialUserBind:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemSocialUserBind=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemSocialUserBind:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemSocialUserBind=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemSocialUserBind.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemSocialUserBind.id==id,SystemSocialUserBind.userId==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemSocialUserBind.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemSocialUserBind.id.in_(ids),SystemSocialUserBind.userId==self.UserId])
    async def GetBindingUsers(self,userId)->List[SystemSocialUserBind]:
        return await self.QueryWhere([SystemSocialUserBind.userId==userId,SystemSocialUserBind.deleted==0])
    async def GetBySocial(self,socialType,socialId)->SystemSocialUserBind:
        return await self.QueryOne([SystemSocialUserBind.socialType==socialType,SystemSocialUserBind.socialUserId==socialId,SystemSocialUserBind.deleted==0])
    async def AddBinding(self,socialType,socialId,userId)->SystemSocialUserBind:
        entity = SystemSocialUserBind()
        entity.userId= userId
        entity.userType = 1
        entity.socialType = socialType
        entity.socialUserId = socialId
        entity.deleted = 0
        await self.Insert(entity)
        return entity

