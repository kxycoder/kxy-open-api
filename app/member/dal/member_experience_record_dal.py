import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.member.models.member_experience_record import MemberExperienceRecord
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class MemberExperienceRecordDal(MyBaseDal[MemberExperienceRecord]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(MemberExperienceRecord,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[MemberExperienceRecord]:
        return await self.QueryWhere([MemberExperienceRecord.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[MemberExperienceRecord],int]:
        fil = list()
        fil.append(MemberExperienceRecord.deleted == 0)
        for k,v in search.items():
            if hasattr(MemberExperienceRecord,k) and v:
                fil.append(getattr(MemberExperienceRecord,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MemberExperienceRecord.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MemberExperienceRecord.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(MemberExperienceRecord.DicType.ilike("%" + search_text + "%"),
            #                  MemberExperienceRecord.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, MemberExperienceRecord.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[MemberExperienceRecord]:
        fil = list()
        fil.append( MemberExperienceRecord.deleted == 0)
        for k,v in search.items():
            if hasattr(MemberExperienceRecord,k) and v:
                fil.append(getattr(MemberExperienceRecord,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( MemberExperienceRecord.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( MemberExperienceRecord. == int(status))
        items = await self.page_fields_nocount_query( MemberExperienceRecord.get_mini_fields(), fil,  MemberExperienceRecord.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->MemberExperienceRecord:
        entity = MemberExperienceRecord()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->MemberExperienceRecord:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MemberExperienceRecord=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([MemberExperienceRecord.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([MemberExperienceRecord.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[MemberExperienceRecord],int]:
        fil = list()
        fil.append(MemberExperienceRecord.userId == self.UserId)
        fil.append(MemberExperienceRecord.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MemberExperienceRecord.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MemberExperienceRecord.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, MemberExperienceRecord.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->MemberExperienceRecord:
        entity = MemberExperienceRecord()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.userId=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->MemberExperienceRecord:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MemberExperienceRecord=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([MemberExperienceRecord.id==id,MemberExperienceRecord.userId==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([MemberExperienceRecord.id.in_(ids),MemberExperienceRecord.userId==self.UserId])
