import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_dept import SystemDept
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemDeptDal(MyBaseDal[SystemDept]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemDept,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemDept],int]:
        fil = list()
        fil.append(SystemDept.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemDept,k) and v:
                fil.append(getattr(SystemDept,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemDept.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemDept.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemDept.DicType.ilike("%" + search_text + "%"),
            #                  SystemDept.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemDept.status == int(status))
        items, total_count = await self.paginate_query(fil, SystemDept.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemDept],int]:
        fil = list()
        fil.append(SystemDept.UID == self.UserId)
        fil.append(SystemDept.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemDept.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemDept.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemDept.status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemDept.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemDept]:
        fil = list()
        fil.append( SystemDept.deleted == 0)
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemDept.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemDept.status == int(status))
        items = await self.page_fields_nocount_query( SystemDept.get_mini_fields(), fil,  SystemDept.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemDept:
        entity = SystemDept()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemDept:
        entity = SystemDept()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemDept:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemDept=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemDept:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemDept=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemDept.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemDept.id==id,SystemDept.UID==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemDept.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemDept.id.in_(ids),SystemDept.UID==self.UserId])