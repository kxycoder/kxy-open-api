# coding=UTF-8

from app.common.basedal import BaseDal
from kxy.framework.friendly_exception import FriendlyException
from sqlalchemy.ext.asyncio import AsyncSession
from app.system.models.sys_menu import MgMenu
from sqlalchemy import and_,or_
from typing import List as TypeList
import re

class SysMenuDal(BaseDal[MgMenu]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__(MgMenu,db,**kwargs)

    # 获取列表
    async def List(self,search, page_index, page_size):
        fil = list()

        # fil.append(MgMenu.Status != 10)
        if search:
           if re.search(r"^(\d)*$", search):
               fil.append(MgMenu.Id == int(search))
           else:
               search =search.strip()
               fil.append(MgMenu.Name.ilike("%" + search + "%"))
        return await self.paginate_query(fil, MgMenu.CreateDate.desc(), page_index, page_size)
    # 创建
    
    async def AddByJsonData(self, jsonData):
        entity = MgMenu()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        await self.Insert(entity)
        return entity    
    async def DeleteChildren(self,parentMenuId):
        await self.TrueDelWhere([MgMenu.ParentId==parentMenuId])
    async def GetSelfAndChildrens(self,id):
        return await self.QueryWhere([or_(MgMenu.ParentId==id,MgMenu.Id==id)])
    async def Delete(self,id):
        # exist=await self.Get(id)
        await self.DeleteChildren(id)
        await self.TrueDel(id)
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
    async def GetMeus(self,systemcode,menuSchemas,isdisplay=None)->TypeList[MgMenu]:
        fil=[]
        if isdisplay is not None:
            fil.append(MgMenu.IsDisplay==isdisplay)
        fil.append(MgMenu.Schema.in_(menuSchemas))
        fil.append(MgMenu.SystemCode==systemcode)
        return await self.QueryWhere(fil)
    async def GetAllMenus(self,systemcode)->TypeList[MgMenu]:
        fil=[]
        fil.append(MgMenu.SystemCode==systemcode)
        return await self.QueryWhere(fil)
        
    async def GetMenu(self,systemcode,schema)->MgMenu:
        fil=[]
        fil.append(MgMenu.Schema==schema)
        fil.append(MgMenu.SystemCode==systemcode)
        return await self.QueryOne(fil)
    async def GetMenuByName(self,systemcode,menuName):
        return await self.QueryOne([MgMenu.Name==menuName,MgMenu.SystemCode==systemcode])

    async def GetSystemMenus(self,systemcode):
        return await self.QueryWhere([MgMenu.SystemCode==systemcode])
    async def GetLastUpdateMenu(self,systemcode,lastTime,endTime):
        fil = list()
        fil.append(MgMenu.SystemCode==systemcode)
        fil.append(or_(and_(MgMenu.LastModifiedDate>=lastTime,MgMenu.LastModifiedDate<endTime),and_(MgMenu.LastModifiedDate==None,MgMenu.CreateDate>=lastTime)))
        return await self.QueryWhere(fil)            
    async def SyncJsonData(self,jsonData):     
        exist=await self.Get(jsonData['Id'])   
        if exist:
            exist.InitInsertEntityWithJson(jsonData)
            await self.Update(exist)
        else:
            exist = MgMenu()
            exist.InitInsertEntityWithJson(jsonData)
            await self.Insert(exist)        