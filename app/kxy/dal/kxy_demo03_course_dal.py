import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.kxy.models.kxy_demo03_course import KxyDemo03Course
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class KxyDemo03CourseDal(MyBaseDal[KxyDemo03Course]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(KxyDemo03Course,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[KxyDemo03Course]:
        return await self.QueryWhere([KxyDemo03Course.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[KxyDemo03Course],int]:
        fil = list()
        fil.append(KxyDemo03Course.deleted == 0)
        for k,v in search.items():
            if hasattr(KxyDemo03Course,k) and v:
                fil.append(getattr(KxyDemo03Course,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(KxyDemo03Course.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(KxyDemo03Course.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(KxyDemo03Course.DicType.ilike("%" + search_text + "%"),
            #                  KxyDemo03Course.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_fields_query(KxyDemo03Course.get_mini_fields(), fil, KxyDemo03Course.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[KxyDemo03Course]:
        fil = list()
        fil.append( KxyDemo03Course.deleted == 0)
        for k,v in search.items():
            if hasattr(KxyDemo03Course,k) and v:
                fil.append(getattr(KxyDemo03Course,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( KxyDemo03Course.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( KxyDemo03Course. == int(status))
        items = await self.page_fields_nocount_query( KxyDemo03Course.get_mini_fields(), fil,  KxyDemo03Course.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->KxyDemo03Course:
        entity = KxyDemo03Course()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->KxyDemo03Course:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:KxyDemo03Course=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([KxyDemo03Course.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([KxyDemo03Course.id.in_(ids)])

    async def DeleteByParentId(self,parentId):
        return await self.DeleteWhere([KxyDemo03Course.studentId==parentId])
    async def AddChildrenBatch(self,parentId,rows:List[Dict[str,object]])->List[KxyDemo03Course]:
        entities = []
        for row in rows:
            entity = KxyDemo03Course()
            entity.InitInsertEntityWithJson(row)
            entity.studentId = parentId
            entity.deleted = 0
            entities.append(entity)
        await self.BatchInsert(entities)
        return entities

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
                    entity = KxyDemo03Course()
                    entity.InitInsertEntityWithJson(row)
                    entity.studentId = parentId
                    entity.deleted = 0
                    entities.append(entity)
            if entities:
                await self.BatchInsert(entities)
        
    async def GetListByParentId(self,parentId)->List[KxyDemo03Course]:
        return await self.QueryWhere([KxyDemo03Course.studentId==parentId,KxyDemo03Course.deleted==0])
 
