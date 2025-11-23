import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.member.models.member_sign_in_record import MemberSignInRecord
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class MemberSignInRecordDal(MyBaseDal[MemberSignInRecord]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(MemberSignInRecord,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[MemberSignInRecord]:
        return await self.QueryWhere([MemberSignInRecord.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[MemberSignInRecord],int]:
        fil = list()
        fil.append(MemberSignInRecord.deleted == 0)
        for k,v in search.items():
            if hasattr(MemberSignInRecord,k) and v:
                fil.append(getattr(MemberSignInRecord,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MemberSignInRecord.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MemberSignInRecord.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(MemberSignInRecord.DicType.ilike("%" + search_text + "%"),
            #                  MemberSignInRecord.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, MemberSignInRecord.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[MemberSignInRecord]:
        fil = list()
        fil.append( MemberSignInRecord.deleted == 0)
        for k,v in search.items():
            if hasattr(MemberSignInRecord,k) and v:
                fil.append(getattr(MemberSignInRecord,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( MemberSignInRecord.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( MemberSignInRecord. == int(status))
        items = await self.page_fields_nocount_query( MemberSignInRecord.get_mini_fields(), fil,  MemberSignInRecord.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->MemberSignInRecord:
        entity = MemberSignInRecord()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->MemberSignInRecord:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MemberSignInRecord=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([MemberSignInRecord.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([MemberSignInRecord.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[MemberSignInRecord],int]:
        fil = list()
        fil.append(MemberSignInRecord.userId == self.UserId)
        fil.append(MemberSignInRecord.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MemberSignInRecord.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MemberSignInRecord.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, MemberSignInRecord.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->MemberSignInRecord:
        entity = MemberSignInRecord()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.userId=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->MemberSignInRecord:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MemberSignInRecord=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([MemberSignInRecord.id==id,MemberSignInRecord.userId==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([MemberSignInRecord.id.in_(ids),MemberSignInRecord.userId==self.UserId])
