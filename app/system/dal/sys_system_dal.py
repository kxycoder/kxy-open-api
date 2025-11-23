# coding=UTF-8

from app.common.basedal import BaseDal
from kxy.framework.friendly_exception import FriendlyException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, and_
from app.system.models.sys_system import MgSystem
import re

class  SysSystemDal(BaseDal[ MgSystem]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__( MgSystem,db,**kwargs)

    # 获取列表
    async def List(self, search, roles,page_index, page_size):
        fil = list()
        if 'admin' not in roles:
            fil.append(MgSystem.SystemCode!='opt_sso')
        fil.append(MgSystem.Status != 10)
        if search:
            if re.search(r"^(\d)*$", search):
                fil.append(MgSystem.Id == int(search))
            else:
                search = search.strip()
                fil.append(or_(MgSystem.Name.ilike("%" + search + "%"),
                               MgSystem.Description.ilike("%" + search + "%"),
                               MgSystem.SystemCode.ilike("%" + search + "%"),
                               ))
        return await self.paginate_query(fil, MgSystem.CreateDate.desc(), page_index, page_size)
    # 创建
    async def GetListBy(self,systemcodes):
        return await self.QueryWhere([MgSystem.SystemCode.in_(systemcodes)])
    async def AddByJsonData(self, jsonData):
        entity = MgSystem()
        entity.InitInsertEntityWithJson(jsonData)
        exist=await self.GetBySystemCode(entity.SystemCode)
        if exist:
            raise FriendlyException('已经存在SystemCode为{}的数据'.format(entity.SystemCode))
        entity.Status = 1
        await self.Insert(entity)
        return entity
    async def GetBySystemCode(self,systemcode):
        return await self.QueryOne([MgSystem.SystemCode == systemcode])
        
    async def Delete(self, id):
        # await self.TrueDel(id)
        exist =await self.Get(id)
        if exist != None:
            exist.Status = 10
            await self.Update(exist)
        else:
            raise FriendlyException('不存在'+str(id)+'的数据')

    async def UpdateByJsonData(self, jsonData)->MgSystem:
        id = jsonData.get('Id', None)
        if id == None:
            raise FriendlyException('更新时必须传回主键')
        entity = await self.Get(id)
        if not entity:
            raise FriendlyException('不存在'+str(id)+"的数据")
        entity.InitUpdateFiles(jsonData)
        await self.Update(entity)
        return entity
    async def GetLastUpdateMenu(self,lastTime,endTime):     
        fil = list()
        fil.append(or_(and_(MgSystem.LastModifiedDate>=lastTime,MgSystem.LastModifiedDate<endTime),and_(MgSystem.LastModifiedDate==None,MgSystem.CreateDate>=lastTime)))
        return await self.QueryWhere(fil)

    async def SyncJsonData(self,jsonData):
        exist=await self.GetBySystemCode(jsonData['SystemCode'])
        if exist:
            exist.Name=jsonData['Name']
            exist.Description=jsonData['Description']
            await self.Update(exist)
        else:
            exist = MgSystem()
            exist.InitInsertEntityWithJson(jsonData)
            await self.Insert(exist)
    async def GetAllSystem(self):
        return await self.QueryWhere([MgSystem.Status == 1])