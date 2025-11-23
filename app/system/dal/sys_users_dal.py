from datetime import datetime
import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select
from app.common.crypto_util import Crypto
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.sys_users import SysUsers
from app.tools import utils
from app.common.basedal import BaseDal


class SysUsersDal(BaseDal[SysUsers]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__(SysUsers,db,**kwargs)
    
    # 获取列表
    async def Search(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        fil.append(SysUsers.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SysUsers.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SysUsers.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SysUsers.Status == int(status))
        items, total_count = await self.paginate_query( fil, SysUsers.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        fil.append(SysUsers.UID == self.UserId)
        fil.append(SysUsers.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SysUsers.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SysUsers.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SysUsers.Status == int(status))
        items, total_count = await self.paginate_query( fil, SysUsers.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def GetUserByOpenId(self,openId)->SysUsers:
        fil = list()
        fil.append(SysUsers.OpenId==openId)
        fil.append(SysUsers.IsDelete==0)
        fil.append(SysUsers.Status==1)
        result =  await self.QueryOne(fil)
        return result
    async def AddByJsonData(self, jsonData)->SysUsers:
        entity = SysUsers()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SysUsers:
        entity = SysUsers()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SysUsers:
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SysUsers=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity
    async def SetHeadImage(self,url):
        await self.UpdateFields([SysUsers.Id== self.UserId],{SysUsers.ImageUrl.key:url})
        
    async def UpdateByJsonDataUser(self,jsonData)->SysUsers:
        '''更新客户自己的数据'''
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SysUsers=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.UpdateFields([SysUsers.Id==id],{'IsDelete':1})

    async def DeleteByUser(self,id):
        await self.UpdateFields([SysUsers.Id==id,SysUsers.UID==self.UserId],{'IsDelete':1})
    async def RegistByOpenId(self,openId, phone,sourceUser='',sourceId='',sourceType='')->SysUsers:
        exist = SysUsers()
        exist.Username = openId[0:10]
        exist.OpenId = openId
        exist.Status=1
        exist.IsDelete= 0 
        exist.IsActive = 1
        exist.ChineseName = openId[0:10]
        lastName = openId[-4:]
        exist.NickName = utils.generateNickName(lastName)
        exist.PhoneNumber = phone
        exist.RegistFrom = sourceUser
        exist.LastLoginDate = datetime.now()
        exist.SourceType = sourceType
        exist.SourceId= sourceId
        await self.Insert(exist)
        return exist
    
    async def Login(self,phoneNumber,password)->SysUsers:
        fil = [
            SysUsers.PhoneNumber == phoneNumber,
            SysUsers.Password == password,
            SysUsers.IsDelete == 0,
            SysUsers.IsActive == 1,
        ]

        result = await self.session.execute(
            select(SysUsers).filter(*fil).limit(1)
        )
        user = result.scalar()

        if user:
            user.LastLoginDate = datetime.now()  # 直接修改属性
            await self.session.commit()  
            await self.Update(user)
        return user
    async def GetCurrentUser(self)->SysUsers:
        return await self.GetExist(self.UserId)
    async def GetUserByPhone(self,phone):
        result = await self.session.execute(select(SysUsers).filter(SysUsers.PhoneNumber == phone).limit(1))
        self.session.commit()
        return result.first()
    async def AddNewUser(self,userName,password,phone)->SysUsers:
        exist = await self.GetUserByPhone(phone)
        if exist:
            raise FriendlyException('手机号已存在')
        user = SysUsers()
        user.Username = userName
        # user.OpenId = 
        user.Status=1
        user.IsDelete= 0 
        user.ChineseName = userName
        user.Password =Crypto().encrypt(password)
        user.IsActive = 1
        user.PhoneNumber = phone
        await self.Insert(user)
        return user
    async def GetUserPhone(self,userId)->str:
        return await self.QueryOne([SysUsers.Id==userId,SysUsers.IsDelete==0,SysUsers.IsActive==1],[SysUsers.Id,SysUsers.PhoneNumber])
    async def GetByUserName(self,userName):
        return await self.QueryOne([SysUsers.Username==userName,SysUsers.IsDelete==0,SysUsers.IsActive==1])
    async def GetSimpleList(self,search,page_index, page_size):
        fil = list()
        fil.append(SysUsers.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SysUsers.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SysUsers.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SysUsers.Status == int(status))
        items, total_count = await self.paginate_fields_query(SysUsers.get_simple_fields(),fil, SysUsers.CreateDate.desc(), page_index, page_size)
        return items, total_count