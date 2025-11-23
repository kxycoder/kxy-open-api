import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.member.models.member_level_record import MemberLevelRecord
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class MemberLevelRecordDal(MyBaseDal[MemberLevelRecord]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(MemberLevelRecord,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[MemberLevelRecord]:
        return await self.QueryWhere([MemberLevelRecord.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[MemberLevelRecord],int]:
        fil = list()
        fil.append(MemberLevelRecord.deleted == 0)
        for k,v in search.items():
            if hasattr(MemberLevelRecord,k) and v:
                fil.append(getattr(MemberLevelRecord,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MemberLevelRecord.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MemberLevelRecord.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(MemberLevelRecord.DicType.ilike("%" + search_text + "%"),
            #                  MemberLevelRecord.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, MemberLevelRecord.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[MemberLevelRecord]:
        fil = list()
        fil.append( MemberLevelRecord.deleted == 0)
        for k,v in search.items():
            if hasattr(MemberLevelRecord,k) and v:
                fil.append(getattr(MemberLevelRecord,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( MemberLevelRecord.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( MemberLevelRecord. == int(status))
        items = await self.page_fields_nocount_query( MemberLevelRecord.get_mini_fields(), fil,  MemberLevelRecord.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->MemberLevelRecord:
        entity = MemberLevelRecord()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->MemberLevelRecord:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MemberLevelRecord=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([MemberLevelRecord.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([MemberLevelRecord.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[MemberLevelRecord],int]:
        fil = list()
        fil.append(MemberLevelRecord.userId == self.UserId)
        fil.append(MemberLevelRecord.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MemberLevelRecord.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MemberLevelRecord.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, MemberLevelRecord.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->MemberLevelRecord:
        entity = MemberLevelRecord()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.userId=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->MemberLevelRecord:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MemberLevelRecord=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([MemberLevelRecord.id==id,MemberLevelRecord.userId==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([MemberLevelRecord.id.in_(ids),MemberLevelRecord.userId==self.UserId])
