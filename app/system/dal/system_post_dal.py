import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_post import SystemPost
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemPostDal(MyBaseDal[SystemPost]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemPost,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemPost],int]:
        fil = list()
        fil.append(SystemPost.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemPost,k) and v:
                fil.append(getattr(SystemPost,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemPost.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemPost.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemPost.DicType.ilike("%" + search_text + "%"),
            #                  SystemPost.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemPost.status == int(status))
        items, total_count = await self.paginate_query(fil, SystemPost.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemPost],int]:
        fil = list()
        fil.append(SystemPost.UID == self.UserId)
        fil.append(SystemPost.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemPost.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemPost.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemPost.status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemPost.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemPost]:
        fil = list()
        fil.append( SystemPost.deleted == 0)
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemPost.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemPost.status == int(status))
        items = await self.page_fields_nocount_query( SystemPost.get_mini_fields(), fil,  SystemPost.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemPost:
        entity = SystemPost()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemPost:
        entity = SystemPost()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemPost:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemPost=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemPost:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemPost=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemPost.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemPost.id==id,SystemPost.UID==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemPost.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemPost.id.in_(ids),SystemPost.UID==self.UserId])
    async def GetByIds(self,ids):
        return await self.QueryWhere([SystemPost.id.in_(ids)])