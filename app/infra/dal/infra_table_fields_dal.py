import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.infra.models.infra_table_fields import InfraTableFields
from app.infra.types.Fields import Field
from app.tools import utils

from app.common.basedal import MyBaseDal

class InfraTableFieldsDal(MyBaseDal[InfraTableFields]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(InfraTableFields,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[InfraTableFields],int]:
        fil = list()
        fil.append(InfraTableFields.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraTableFields,k) and v:
                fil.append(getattr(InfraTableFields,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(InfraTableFields.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(InfraTableFields.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(InfraTableFields.DicType.ilike("%" + search_text + "%"),
            #                  InfraTableFields.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(InfraTableFields.Status == int(status))
        items, total_count = await self.paginate_query(fil, InfraTableFields.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[InfraTableFields],int]:
        fil = list()
        fil.append(InfraTableFields.UID == self.UserId)
        fil.append(InfraTableFields.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(InfraTableFields.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(InfraTableFields.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(InfraTableFields.Status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, InfraTableFields.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[InfraTableFields]:
        fil = list()
        fil.append( InfraTableFields.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraTableFields,k) and v:
                fil.append(getattr(InfraTableFields,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( InfraTableFields.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( InfraTableFields.Status == int(status))
        items = await self.page_fields_nocount_query( InfraTableFields.get_mini_fields(), fil,  InfraTableFields.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->InfraTableFields:
        entity = InfraTableFields()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->InfraTableFields:
        entity = InfraTableFields()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->InfraTableFields:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:InfraTableFields=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->InfraTableFields:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:InfraTableFields=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([InfraTableFields.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([InfraTableFields.id==id,InfraTableFields.UID==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([InfraTableFields.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([InfraTableFields.id.in_(ids),InfraTableFields.UID==self.UserId])
    def generate_fields(self,tableId,field:Field):
        entity = InfraTableFields()
        entity.tableId= tableId
        entity.fieldName= field.FieldName
        entity.isPrimaryKey= field.IsPrimaryKey
        entity.isAutoIncrement= field.IsAutoIncrement
        entity.canNull= field.CanNull
        entity.dataType= field.DataType
        entity.description= field.Description
        entity.length= field.Length
        entity.showInTable= field.ShowInTable
        entity.showInForm= field.ShowInForm
        entity.showDetail= field.ShowDetail
        entity.showInSerch= field.ShowInSerch
        return entity
    async def AddFields(self,tableId,fields:List[Field]):
        entities = []
        for field in fields:
            entity = self.generate_fields(tableId,field)
            entities.append(entity)
        await self.BatchInsert(entities)
    async def DeleteByTableId(self,id):
        await self.DeleteWhere([InfraTableFields.tableId==id])
    async def GetFields(self,tbleId)->List[InfraTableFields]:
        return await self.QueryWhere([InfraTableFields.tableId==tbleId,InfraTableFields.deleted==0])
    async def GetFieldNames(self,tbleId)->List[InfraTableFields]:
        return await self.QueryWhere([InfraTableFields.tableId==tbleId,InfraTableFields.deleted==0],fields=[InfraTableFields.id, InfraTableFields.fieldName,InfraTableFields.description])
    async def UpdateByJsonDataFields(self,tableId,rows)->List[InfraTableFields]:
        async with self as dal:
            self.AutoCommit = False
            entities = []
            for row in rows:
                entity = InfraTableFields()
                entity.InitInsertEntityWithJson(row)    
                entities.append(entity)
            await dal.DeleteByTableId(tableId)
            await dal.BatchInsert(entities)
            return entities