import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.infra.models.infra_template_file import InfraTemplateFile
from app.tools import utils

from app.common.basedal import MyBaseDal

class InfraTemplateFileDal(MyBaseDal[InfraTemplateFile]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(InfraTemplateFile,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[InfraTemplateFile],int]:
        fil = list()
        fil.append(InfraTemplateFile.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraTemplateFile,k) and v:
                fil.append(getattr(InfraTemplateFile,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(InfraTemplateFile.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(InfraTemplateFile.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(InfraTemplateFile.DicType.ilike("%" + search_text + "%"),
            #                  InfraTemplateFile.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(InfraTemplateFile.Status == int(status))
        items, total_count = await self.paginate_query(fil, InfraTemplateFile.createTime.desc(), page_index, page_size)
        return items, total_count
    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[InfraTemplateFile]:
        fil = list()
        fil.append( InfraTemplateFile.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraTemplateFile,k) and v:
                fil.append(getattr(InfraTemplateFile,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( InfraTemplateFile.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( InfraTemplateFile.Status == int(status))
        items = await self.page_fields_nocount_query( InfraTemplateFile.get_mini_fields(), fil,  InfraTemplateFile.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->InfraTemplateFile:
        entity = InfraTemplateFile()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.deleted = 0
        await self.Insert(entity)
        return entity
    async def AddChildrenBatch(self,parentId,rows:List[Dict[str,object]])->List[InfraTemplateFile]:
        entities = []
        for row in rows:
            entity = InfraTemplateFile()
            entity.InitInsertEntityWithJson(row)
            entity.templateId = parentId
            entity.deleted = 0
            entities.append(entity)
        await self.BatchInsert(entities)
        return entities
    async def DeleteByParentId(self,parentId):
        return await self.DeleteWhere([InfraTemplateFile.templateId==parentId])
    async def UpdateChildrenBatch(self,parentId,rows:List[Dict[str,object]]):
        exists = await self.GetListByParentId(parentId)
        exist_dict = {x.id:x for x in exists}
        entities = []
        self.AutoCommit = False
        async with self.session.begin() as tran:
            for row in rows:
                id = row.get('id')
                if id:
                    if id not in exist_dict:
                        raise FriendlyException('数据问题，请刷新界面再操作')
                    exist = exist_dict[id]
                    exist.InitUpdateFiles(row)
                    await self.Update(entity)
                else:
                    entity = InfraTemplateFile()
                    entity.InitInsertEntityWithJson(row)
                    entity.templateId = parentId
                    entity.deleted = 0
                    entities.append(entity)
            if entities:
                await self.BatchInsert(entities)
        
    async def GetListByParentId(self,parentId)->List[InfraTemplateFile]:
        return await self.QueryWhere([InfraTemplateFile.templateId==parentId,InfraTemplateFile.deleted==0])
        
    async def UpdateByJsonData(self,jsonData)->InfraTemplateFile:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:InfraTemplateFile=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([InfraTemplateFile.id==id])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([InfraTemplateFile.id.in_(ids)])

    async def GetFiles(self,templateId,fileId=0):
        fil=[InfraTemplateFile.templateId==templateId,InfraTemplateFile.deleted==0]
        if fileId:
            fil=[InfraTemplateFile.id==fileId]
        return await self.QueryWhere(fil,orderBy=InfraTemplateFile.createTime.desc())
    async def DeleteByTemplateId(self,templateId):
        return await self.DeleteWhere([InfraTemplateFile.templateId==templateId])