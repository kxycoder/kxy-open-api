import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_user_post import SystemUserPost
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemUserPostDal(MyBaseDal[SystemUserPost]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemUserPost,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemUserPost],int]:
        fil = list()
        fil.append(SystemUserPost.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemUserPost,k) and v:
                fil.append(getattr(SystemUserPost,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemUserPost.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemUserPost.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemUserPost.DicType.ilike("%" + search_text + "%"),
            #                  SystemUserPost.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemUserPost.Status == int(status))
        items, total_count = await self.paginate_query(fil, SystemUserPost.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemUserPost],int]:
        fil = list()
        fil.append(SystemUserPost.userId == self.UserId)
        fil.append(SystemUserPost.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemUserPost.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemUserPost.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemUserPost.Status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemUserPost.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemUserPost]:
        fil = list()
        fil.append( SystemUserPost.deleted == 0)
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemUserPost.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemUserPost.Status == int(status))
        items = await self.page_fields_nocount_query( SystemUserPost.get_mini_fields(), fil,  SystemUserPost.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemUserPost:
        entity = SystemUserPost()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemUserPost:
        entity = SystemUserPost()
        entity.InitInsertEntityWithJson(jsonData)
        entity.userId=self.UserId
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemUserPost:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemUserPost=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemUserPost:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemUserPost=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemUserPost.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemUserPost.id==id,SystemUserPost.userId==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemUserPost.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemUserPost.id.in_(ids),SystemUserPost.userId==self.UserId])