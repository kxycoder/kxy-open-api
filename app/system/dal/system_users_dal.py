from datetime import datetime
import json
import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.filter import ignore_filter
from app.contract.types.user_vo import VoUserInfo, VoUserProfilePass
from app.common.crypto_util import Crypto
from app.system.models.system_users import SystemUsers
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemUsersDal(MyBaseDal[SystemUsers]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemUsers,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemUsers],int]:
        fil = list()
        fil.append(SystemUsers.deleted == 0)
        search_text=search.get('search')
        for k,v in search.items():
            if hasattr(SystemUsers,k) and v:
                fil.append(getattr(SystemUsers,k).ilike(f'%{v}%'))
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemUsers.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemUsers.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemUsers.DicType.ilike("%" + search_text + "%"),
            #                  SystemUsers.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemUsers.status == int(status))
        items, total_count = await self.paginate_fields_query(SystemUsers.get_mini_fields(),fil, SystemUsers.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemUsers]:
        fil = list()
        fil.append( SystemUsers.deleted == 0)
        items = await self.page_fields_nocount_query(SystemUsers.get_mini_fields(), fil, SystemUsers.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemUsers:
        entity = SystemUsers()
        entity.InitInsertEntityWithJson(jsonData)
        entity.status = 0
        entity.deleted = 0
        password = jsonData.get('password',None)
        entity.password = Crypto().encrypt(password)
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemUsers:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemUsers=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity
    
    async def UpdateMyprofile(self,jsonData)->SystemUsers:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        if id!=self.UserId:
            raise FriendlyException('只能修改自己的数据')
        entity:SystemUsers=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemUsers.id==id])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemUsers.id.in_(ids)])
    @ignore_filter
    async def Login(self,userName,password)->SystemUsers:
        fil = [
            SystemUsers.username == userName,
            SystemUsers.password == password,
            SystemUsers.deleted == 0,
            SystemUsers.status == 0,
        ]

        user = await self.QueryOne(fil)

        if user:
            user.loginDate = datetime.now()  # 直接修改属性
            await self.session.commit()  
            await self.Update(user)
        return user
    async def GetCurrentUser(self):
        return await self.QueryOne([SystemUsers.id == self.UserId])
    async def UpdatePassword(self,userInfo:VoUserInfo):
        await self.UpdateFields([SystemUsers.id==userInfo.id],{"password":Crypto().encrypt(userInfo.password)})

    async def UpdateMyPassword(self,userInfo:VoUserProfilePass):
        currentUser = await self.GetCurrentUser()
        oldPassword = Crypto().encrypt(userInfo.oldPassword)
        if currentUser.password != oldPassword:
            raise FriendlyException('旧密码错误')
        currentUser.password = Crypto().encrypt(userInfo.newPassword)
        await self.Update(currentUser)
    async def UpdateUserStatus(self,userid,status):
        await self.UpdateFields([SystemUsers.id==userid],{"status":status})
    @ignore_filter
    async def AddUser(self,username,nickName,password,contactMobile,tenantId)->SystemUsers:
        entity = SystemUsers()
        entity.username = username
        entity.nickname = nickName
        entity.password = Crypto().encrypt(password)
        entity.mobile = contactMobile
        entity.status = 0
        entity.deleted = 0
        entity.tenantId = tenantId
        
        await self.Insert(entity)
        return entity
    @ignore_filter
    async def DeleteByTenantId(self,tenantId):
        return await self.DeleteWhere([SystemUsers.tenantId==tenantId])
    @ignore_filter
    async def GetUserName(self,username)->SystemUsers:
        return await self.QueryOne([SystemUsers.username==username,SystemUsers.deleted==0],fields=[SystemUsers.id])
    
    async def GetUserByIds(self,ids)->List[SystemUsers]:
        return await self.QueryWhere([SystemUsers.id.in_(ids),SystemUsers.deleted==0],fields = SystemUsers.get_mini_fields())