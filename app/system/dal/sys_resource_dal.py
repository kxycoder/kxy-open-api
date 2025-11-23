# coding=UTF-8

from app.common.basedal import BaseDal
from kxy.framework.friendly_exception import FriendlyException
from sqlalchemy.ext.asyncio import AsyncSession
from app.system.models.sys_resource import MgResource
from sqlalchemy import or_, and_
import re

class SysResourceDal(BaseDal[MgResource]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__(MgResource,db,**kwargs)

    # 获取列表
    async def List(self,search, menuid,page_index, page_size):
        fil = list()

        # fil.append(MgResource.Status != 10)
        if search:
           if re.search(r"^(\d)*$", search):
               fil.append(MgResource.Id == int(search))
           else:
               search =search.strip()
               fil.append(MgResource.Description.ilike("%" + search + "%"))
        if menuid:
            fil.append(MgResource.MenuId==menuid)

        return await self.paginate_query(fil, MgResource.CreateDate.desc(), page_index, page_size)
    # 创建

    async def AddByJsonData(self, jsonData):
        entity = MgResource()
        entity.InitInsertEntityWithJson(jsonData)    
        # entity.Status = 1
        # entity.Id=None
        entity.Name=entity.Description
        await self.Insert(entity)
        return entity
    async def Delete(self,id):
        await self.TrueDel(id)
        # exist=await self.Get(id)
        # if exist!=None:
        #     exist.Status=10
        #     await self.Update(exist)
        # else:
        #     raise FriendlyException('不存在'+str(id)+'的数据')
    async def UpdateByJsonData(self,jsonData):
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity=await self.Get(id)
        if not entity:
            raise FriendlyException('不存在'+str(id)+"的数据")
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def GetSchemaResource(self,MenuId):
        return await self.QueryWhere([MgResource.MenuId==MenuId],[MgResource.Schema,MgResource.Name,MgResource.Description])
    async def Exist(self,menuId,schema):
        exist= await self.QueryOne([MgResource.MenuId==menuId,MgResource.Schema==schema],[MgResource.Id])
        return exist is not None
    async def GetBy(self,MenuId,Schema):
        return await self.QueryOne([MgResource.MenuId==MenuId,MgResource.Schema==Schema])
    async def Add(self,menuId,schema,des='')->MgResource:
        if await self.Exist(menuId,schema):
            raise FriendlyException(f'已经存在{menuId}-{schema}的资源')
        entity = MgResource()
        entity.MenuId=menuId
        entity.Schema=schema
        entity.Description=des if des else schema
        entity.Name=schema
        await self.Insert(entity)
        return entity

    async def GetLastUpdateMenu(self,MenuIds,lastTime,endTime):
        fil = list()
        fil.append(MgResource.MenuId.in_(MenuIds))
        fil.append(or_(and_(MgResource.LastModifiedDate>=lastTime,MgResource.LastModifiedDate<endTime),and_(MgResource.LastModifiedDate==None,MgResource.CreateDate>=lastTime)))
        return await self.QueryWhere(fil)

    async def SyncJsonData(self,jsonData):     
        exist=await self.GetBy(jsonData['MenuId'],jsonData['Schema'])
        if exist:
            exist.Name=jsonData['Name']
            exist.Description=jsonData['Description']
            await self.Update(exist)
        else:
            exist = MgResource()
            exist.InitInsertEntityWithJson(jsonData)
            await self.Insert(exist)
    async def GetMenuResource(self,MenuId):
        return await self.QueryWhere(fil=[MgResource.MenuId==MenuId])
    async def DeleteByMenuId(self,MenuId):
        await self.TrueDelWhere([MgResource.MenuId==MenuId])