from datetime import datetime, timedelta
import re
from typing import Dict,List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.sys_users import SysUsers
from app.system.models.system_oauth2_access_token import SystemOauth2AccessToken
from app.tools import utils
from app.config import config

from app.common.basedal import MyBaseDal

class SystemOauth2AccessTokenDal(MyBaseDal[SystemOauth2AccessToken]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemOauth2AccessToken,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemOauth2AccessToken],int]:
        fil = list()
        fil.append(SystemOauth2AccessToken.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemOauth2AccessToken,k) and v:
                fil.append(getattr(SystemOauth2AccessToken,k)==v)

        items, total_count = await self.paginate_query(fil, SystemOauth2AccessToken.createTime.desc(), page_index, page_size)
        return items, total_count

    async def AddByJsonData(self, jsonData)->SystemOauth2AccessToken:
        entity = SystemOauth2AccessToken()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.deleted = 0
        await self.Insert(entity)
        return entity
    async def UpdateByJsonData(self,jsonData)->SystemOauth2AccessToken:
        id=jsonData.get('status',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemOauth2AccessToken=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.UpdateFields([SystemOauth2AccessToken.status==id],{'deleted':1})
    def newToken(self,token:SystemOauth2AccessToken,refreshToken:str):
        token.accessToken = uuid.uuid4().hex
        token.refreshToken = refreshToken
        token.expiresTime = datetime.now() + timedelta(seconds=config.ACCESS_TOKEN_EXPIRE_SECONDES)
        return token
    async def Clear(self,user_id:int,tenant_id:int):
        await self.DeleteWhere([SystemOauth2AccessToken.userId==user_id,SystemOauth2AccessToken.deleted==0,SystemOauth2AccessToken.tenantId==tenant_id])
    async def CreateToken(self,user_id:int,refreshToken:str, tenant_id:int):
        token = SystemOauth2AccessToken()
        token.clientId='default'
        token.userId = user_id
        self.newToken(token,refreshToken)
        token.refreshToken = refreshToken
        token.userInfo='{}'
        token.userType = 1
        token.tenantId = tenant_id
        await self.Insert(token)
        return token
    async def GetByRefreshToken(self,refresh_token)->SystemOauth2AccessToken:
        return await self.QueryOne([SystemOauth2AccessToken.refreshToken==refresh_token,SystemOauth2AccessToken.deleted==0],orderBy=[SystemOauth2AccessToken.expiresTime.desc()])
    async def DeleteByAccessToken(self,accessToken):
        return await self.DeleteWhere([SystemOauth2AccessToken.accessToken==accessToken,SystemOauth2AccessToken.deleted==0])
        