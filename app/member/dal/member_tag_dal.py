import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.member.models.member_tag import MemberTag
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class MemberTagDal(MyBaseDal[MemberTag]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(MemberTag,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[MemberTag]:
        return await self.QueryWhere([MemberTag.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[MemberTag],int]:
        fil = list()
        fil.append(MemberTag.deleted == 0)
        for k,v in search.items():
            if hasattr(MemberTag,k) and v:
                fil.append(getattr(MemberTag,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MemberTag.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MemberTag.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(MemberTag.DicType.ilike("%" + search_text + "%"),
            #                  MemberTag.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, MemberTag.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[MemberTag]:
        fil = list()
        fil.append( MemberTag.deleted == 0)
        for k,v in search.items():
            if hasattr(MemberTag,k) and v:
                fil.append(getattr(MemberTag,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( MemberTag.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( MemberTag. == int(status))
        items = await self.page_fields_nocount_query( MemberTag.get_mini_fields(), fil,  MemberTag.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->MemberTag:
        entity = MemberTag()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->MemberTag:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MemberTag=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([MemberTag.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([MemberTag.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[MemberTag],int]:
        fil = list()
        fil.append(MemberTag.creator == self.UserId)
        fil.append(MemberTag.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MemberTag.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MemberTag.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, MemberTag.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->MemberTag:
        entity = MemberTag()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->MemberTag:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MemberTag=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([MemberTag.id==id,MemberTag.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([MemberTag.id.in_(ids),MemberTag.creator==self.UserId])
