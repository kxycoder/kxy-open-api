# coding=UTF-8

from app.common.basedal import BaseDal
from kxy.framework.friendly_exception import FriendlyException
from sqlalchemy.ext.asyncio import AsyncSession
from app.system.models.sys_tokens import OptSsoTokens
import re
from uuid import uuid4
from datetime import datetime,timedelta
class SysTokensDal(BaseDal[OptSsoTokens]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__(OptSsoTokens,db,**kwargs)

    # 获取列表
    async def List(self,search, page_index, page_size):
        fil = list()

        fil.append(OptSsoTokens.Status != 10)
        #if search:
        #    if re.search(r"^(\d)*$", search):
        #        fil.append(OptSsoTokens.ID == int(search))
        #    else:
        #        search =search.strip()
        #        fil.append(OptSsoTokens.Name.ilike("%" + search + "%"))
        return await self.paginate_query(fil, OptSsoTokens.CreateDate.desc(), page_index, page_size)
    # 创建

    async def AddByJsonData(self, jsonData):
        entity = OptSsoTokens()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        await self.Insert(entity)
        return entity
    async def Delete(self,id):
        exist=await self.Get(id)
        if exist!=None:
            exist.Status=10
            await self.Update(exist)
        else:
            raise FriendlyException('不存在'+str(id)+'的数据')
    async def UpdateByJsonData(self,jsonData):
        id=jsonData.get('Token',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity=await self.Get(id)
        if not entity:
            raise FriendlyException('不存在'+str(id)+"的数据")
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity
    async def Get(self, id):
        return await self.QueryOne([OptSsoTokens.UserId == id])
    async def GetActiveToken(self,userid):
        now=datetime.now()
        return await self.QueryOne([OptSsoTokens.UserId == userid,OptSsoTokens.Expires>now])

    async def CreateUserToken(self,userid):
        exist=self.GetActiveToken(userid)
        if exist:
            return exist.Token
        token=str(uuid4())
        entity=OptSsoTokens()
        entity.Token=token
        entity.UserId=userid
        entity.Expires=datetime.now()+timedelta(hours=8)
        await self.Insert(entity)

        return token
    async def Auth(self,token):
        return await self.QueryOne([OptSsoTokens.Token == token,OptSsoTokens.Expires>datetime.now()])
