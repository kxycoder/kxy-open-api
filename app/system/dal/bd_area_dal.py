# coding=UTF-8

from sqlalchemy import select
from app.common.basedal import BaseDal
from kxy.framework.friendly_exception import FriendlyException
from sqlalchemy.ext.asyncio import AsyncSession
from app.system.models.sys_area import BdArea
import re

class BdAreaDal(BaseDal[BdArea]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__(BdArea,db,**kwargs)

    # 获取列表
    async def List(self,search,page_index, page_size):
        fil = list()
        # fil.append(BdArea.Status != 10)
        if search.get('Id'):
            fil.append(BdArea.Id==int(search.get('Id')))
        if search.get('Code'):
            fil.append(BdArea.Code==search.get('Code'))
        if search.get('JoinCode'):
            fil.append(BdArea.JoinCode==search.get('JoinCode'))
        if search.get('Name'):
            fil.append(BdArea.Name.ilike(f"%{search.get('Name')}%"))
        if search.get('ParentId'):
            fil.append(BdArea.ParentId==int(search.get('ParentId')))
        if search.get('Level'):
            fil.append(BdArea.Level==int(search.get('Level')))
            
        fields=[BdArea.Id,BdArea.Code,BdArea.JoinCode,BdArea.Name,BdArea.ParentId,BdArea.Level]
        datas, total = await self.paginate_fields_query(fields,fil,BdArea.Id.asc(),page_index,page_size)
        return total,datas
    async def GetChildrens(self,pId:int):
        fields = [BdArea.Id.label("id"),BdArea.Id.label("value"),BdArea.ParentId.label("pId"),BdArea.Name.label('title')]
        fil =[]
        if pId == 0:
            fil.append(BdArea.Level == 2)
        else:
            fil.append(BdArea.ParentId == pId)
        return await self.QueryWhere(fil,fields)
    async def AddByJsonData(self, jsonData):
        entity = BdArea()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        await self.Insert(entity)
        return entity

    async def Delete(self,id):
        await self.Delete(id)

    async def deletebatch(self,ids):
        await self.DeleteBatch(ids)
        
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