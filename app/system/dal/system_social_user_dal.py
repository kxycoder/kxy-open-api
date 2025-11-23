import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.api.types.vo_request import VoSocialUser
from app.system.models.system_social_user import SystemSocialUser
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemSocialUserDal(MyBaseDal[SystemSocialUser]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemSocialUser,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemSocialUser],int]:
        fil = list()
        fil.append(SystemSocialUser.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemSocialUser,k) and v:
                fil.append(getattr(SystemSocialUser,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemSocialUser.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemSocialUser.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemSocialUser.DicType.ilike("%" + search_text + "%"),
            #                  SystemSocialUser.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemSocialUser.Status == int(status))
        items, total_count = await self.paginate_query(fil, SystemSocialUser.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemSocialUser],int]:
        fil = list()
        fil.append(SystemSocialUser.UID == self.UserId)
        fil.append(SystemSocialUser.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemSocialUser.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemSocialUser.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemSocialUser.Status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemSocialUser.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemSocialUser]:
        fil = list()
        fil.append( SystemSocialUser.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemSocialUser,k) and v:
                fil.append(getattr(SystemSocialUser,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemSocialUser.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemSocialUser.Status == int(status))
        items = await self.page_fields_nocount_query( SystemSocialUser.get_mini_fields(), fil,  SystemSocialUser.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemSocialUser:
        entity = SystemSocialUser()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemSocialUser:
        entity = SystemSocialUser()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemSocialUser:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemSocialUser=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemSocialUser:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemSocialUser=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemSocialUser.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemSocialUser.id==id,SystemSocialUser.UID==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemSocialUser.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemSocialUser.id.in_(ids),SystemSocialUser.UID==self.UserId])
    async def GetByOpenId(self,authType,unionid):
        return await self.QueryOne([SystemSocialUser.type==authType,SystemSocialUser.openid==unionid,SystemSocialUser.deleted==0])
    
    async def AddByField(self,authType,data:VoSocialUser):
        entity = SystemSocialUser()
        entity.nickname = data.nickname
        entity.rawUserInfo = data.rawUserInfo
        entity.rawTokenInfo = data.rawToken
        entity.openid = data.unionid
        entity.type = authType
        entity.code = data.code
        entity.state = data.state
        entity.token = data.token
        entity.avatar = data.avatar
        await self.Insert(entity)
        return entity
    async def GetByIds(self,ids)->List[SystemSocialUser]:
        return await self.QueryWhere([SystemSocialUser.id.in_(ids),SystemSocialUser.deleted==0])