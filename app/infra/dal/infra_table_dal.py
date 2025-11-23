import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.infra.models.infra_table import InfraTable
from app.infra.types.Fields import Table
from app.tools import utils

from app.common.basedal import MyBaseDal

class InfraTableDal(MyBaseDal[InfraTable]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(InfraTable,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[InfraTable],int]:
        fil = list()
        fil.append(InfraTable.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraTable,k) and v:
                fil.append(getattr(InfraTable,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(InfraTable.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(InfraTable.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(InfraTable.DicType.ilike("%" + search_text + "%"),
            #                  InfraTable.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(InfraTable.Status == int(status))
        items, total_count = await self.paginate_query(fil, InfraTable.id.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[InfraTable],int]:
        fil = list()
        fil.append(InfraTable.userId == self.UserId)
        fil.append(InfraTable.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(InfraTable.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(InfraTable.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(InfraTable.Status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, InfraTable.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[InfraTable]:
        fil = list()
        fil.append( InfraTable.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraTable,k) and v:
                fil.append(getattr(InfraTable,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( InfraTable.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( InfraTable.Status == int(status))
        items = await self.page_fields_nocount_query( InfraTable.get_mini_fields(), fil,  InfraTable.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->InfraTable:
        entity = InfraTable()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->InfraTable:
        entity = InfraTable()
        entity.InitInsertEntityWithJson(jsonData)
        entity.userId=self.UserId
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->InfraTable:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:InfraTable=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->InfraTable:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:InfraTable=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([InfraTable.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([InfraTable.id==id,InfraTable.userId==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([InfraTable.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([InfraTable.id.in_(ids),InfraTable.userId==self.UserId])
    def genEntity(self,table:Table,databaseName:str,templateId:int,templateParam:str)->InfraTable:
        entity = InfraTable()
        entity.databaseName = databaseName
        entity.tableName = table.TableName
        entity.tableDes = table.TableDes
        entity.primaryKey = table.PrimaryKey.FieldName
        entity.templateId = templateId
        entity.templateParam = templateParam
        return entity
    async def AddByBatch(self,tables:List[Table],databaseName:str,templateId:int,templateParam:str)->List[InfraTable]:
        entities = []
        for table in tables:
            entity = self.genEntity(table,databaseName,templateId,templateParam)
            entities.append(entity)
        await self.BatchInsert(entities)
        return entities
    async def Find(self,databaseName,tableName)->InfraTable:
        return await self.QueryOne([InfraTable.databaseName==databaseName,InfraTable.tableName==tableName,InfraTable.deleted==0])
    async def GetOneTableId(self,templateId,excutions=None)->int:
        '''获取一个用于测试的模板表，优先挑选有子表的表'''
        excutions
        fil =[InfraTable.templateId==templateId, InfraTable.deleted==0]
        if excutions:
            fil.append(InfraTable.pageType.in_(excutions))
        exist = await self.QueryOne(fil,fields=[InfraTable.parentId])
        if exist:
            return exist.id
        else:
            exist = await self.QueryOne([InfraTable.templateId==templateId,InfraTable.deleted==0],fields=[InfraTable.id])
            return exist.id if exist else 0
    async def UpdateDownUrl(self,id,downUrl):
        await self.UpdateFields([InfraTable.id==id],{InfraTable.downUrl.key:downUrl})
    async def GetChildrens(self,parentId:int)->List[InfraTable]:
        return await self.QueryWhere([InfraTable.parentId==parentId,InfraTable.deleted==0])
    async def GetMutiChildrenIds(self,ids:List[int])->List[int]:
        result= await self.QueryWhere([InfraTable.parentId.in_(ids),InfraTable.deleted==0],fields=[InfraTable.id])
        return [item.id for item in result]
    async def GetTableAndChildrenRelations(self,ids:List[int])->List[InfraTable]:
        fil = []
        fil.append(or_(InfraTable.parentId.in_(ids),InfraTable.id.in_(ids)))
        fil.append(InfraTable.deleted==0)
        return await self.QueryWhere(fil,fields=[InfraTable.id,InfraTable.parentId])