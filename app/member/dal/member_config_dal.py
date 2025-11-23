import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.member.models.member_config import MemberConfig
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class MemberConfigDal(MyBaseDal[MemberConfig]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(MemberConfig,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[MemberConfig]:
        return await self.QueryWhere([MemberConfig.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[MemberConfig],int]:
        fil = list()
        fil.append(MemberConfig.deleted == 0)
        for k,v in search.items():
            if hasattr(MemberConfig,k) and v:
                fil.append(getattr(MemberConfig,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MemberConfig.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MemberConfig.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(MemberConfig.DicType.ilike("%" + search_text + "%"),
            #                  MemberConfig.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, MemberConfig.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[MemberConfig]:
        fil = list()
        fil.append( MemberConfig.deleted == 0)
        for k,v in search.items():
            if hasattr(MemberConfig,k) and v:
                fil.append(getattr(MemberConfig,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( MemberConfig.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( MemberConfig. == int(status))
        items = await self.page_fields_nocount_query( MemberConfig.get_mini_fields(), fil,  MemberConfig.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->MemberConfig:
        entity = MemberConfig()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->MemberConfig:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MemberConfig=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([MemberConfig.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([MemberConfig.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[MemberConfig],int]:
        fil = list()
        fil.append(MemberConfig.creator == self.UserId)
        fil.append(MemberConfig.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(MemberConfig.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(MemberConfig.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, MemberConfig.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->MemberConfig:
        entity = MemberConfig()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->MemberConfig:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:MemberConfig=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([MemberConfig.id==id,MemberConfig.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([MemberConfig.id.in_(ids),MemberConfig.creator==self.UserId])
