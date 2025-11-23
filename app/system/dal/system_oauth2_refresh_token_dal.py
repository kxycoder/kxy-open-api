from datetime import datetime, timedelta
import re
from typing import Dict,List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.sys_users import SysUsers
from app.system.models.system_oauth2_refresh_token import SystemOauth2RefreshToken
from app.tools import utils
from app.config import config

from app.common.basedal import MyBaseDal

class SystemOauth2RefreshTokenDal(MyBaseDal[SystemOauth2RefreshToken]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemOauth2RefreshToken,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemOauth2RefreshToken],int]:
        fil = list()
        fil.append(SystemOauth2RefreshToken.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemOauth2RefreshToken,k) and v:
                fil.append(getattr(SystemOauth2RefreshToken,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemOauth2RefreshToken.id == int(search_text))
        items, total_count = await self.paginate_query(fil, SystemOauth2RefreshToken.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemOauth2RefreshToken],int]:
        fil = list()
        fil.append(SystemOauth2RefreshToken.userId == self.UserId)
        fil.append(SystemOauth2RefreshToken.deleted == 0)
        search_text=search.get('search')
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemOauth2RefreshToken.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonData(self, jsonData)->SystemOauth2RefreshToken:
        entity = SystemOauth2RefreshToken()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemOauth2RefreshToken:
        id=jsonData.get('status',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemOauth2RefreshToken=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.UpdateFields([SystemOauth2RefreshToken.status==id],{'deleted':1})

    async def AddRefreshToken(self,user:SysUsers,tenant_id:int,token:str=None)->SystemOauth2RefreshToken:
        token = SystemOauth2RefreshToken()
        token.userId = user.id
        token.refreshToken = token if not token else uuid.uuid4().hex
        token.tenantId = tenant_id
        token.clientId = 'default'
        token.expiresTime = datetime.now() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_SECONDES)
        token.userType = 1
        await self.Insert(token)
        return token
    async def Clear(self,user_id:int,tenant_id:int):
        await self.DeleteWhere([SystemOauth2RefreshToken.userId==user_id,SystemOauth2RefreshToken.deleted==0,SystemOauth2RefreshToken.tenantId==tenant_id])
    async def GetCurrentToken(self,user_id:int,tenant_id:int)->SystemOauth2RefreshToken:
        return await self.QueryOne([SystemOauth2RefreshToken.userId==user_id,SystemOauth2RefreshToken.deleted==0, SystemOauth2RefreshToken.tenantId==tenant_id])
    async def RefreshToken(self,user_id:int,tenant_id:int):
        current = await self.GetCurrentToken(user_id,tenant_id)
        if current:
            if utils.is_expire_after(current.expiresTime,minute=10):
                current.deleted = 1
                await self.Update(current)
            else:
                return current
            
        return await self.AddRefreshToken(user_id,tenant_id)
    async def getUserToken(self,userid,tenant_id)->SystemOauth2RefreshToken:
        return await self.QueryOne([SystemOauth2RefreshToken.userId==userid,SystemOauth2RefreshToken.deleted==0, SystemOauth2RefreshToken.tenantId==tenant_id],orderBy=SystemOauth2RefreshToken.expiresTime.desc())
    async def GetByToken(self,refreshToken)->SystemOauth2RefreshToken:
        return await self.QueryOne([SystemOauth2RefreshToken.refreshToken==refreshToken,SystemOauth2RefreshToken.deleted==0])