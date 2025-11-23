import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_dict_data import SystemDictData
from app.system.models.system_dict_type import SystemDictType
from app.tools import utils
from kxy.framework.filter import ignore_filter
from kxy.framework.context import current_tenant_id

from app.common.basedal import MyBaseDal

class SystemDictTypeDal(MyBaseDal[SystemDictType]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemDictType,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemDictType],int]:
        fil = list()
        fil.append(SystemDictType.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemDictType,k) and v:
                if k == 'name':
                    fil.append(or_(SystemDictType.name.ilike(f'%{v}%'),SystemDictType.type.ilike(f'%{v}%')))
                else:
                    fil.append(getattr(SystemDictType,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemDictType.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemDictType.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemDictType.DicType.ilike("%" + search_text + "%"),
            #                  SystemDictType.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemDictType.status == int(status))
        items, total_count = await self.paginate_query(fil, SystemDictType.createTime.desc(), page_index, page_size)
        return items, total_count
    # def _check_extend_field(self, field_name,value):
    #     if field_name!='_tenant_field':
    #         return super()._check_extend_field(field_name,value)
    #     return SystemDictType.tenantId.in_([1,current_tenant_id.get()])


    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemDictType]:
        fil = list()
        fil.append( SystemDictType.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemDictType,k) and v:
                fil.append(getattr(SystemDictType,k).like(f'%{v}%'))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemDictType.status == int(status))
        items = await self.page_fields_nocount_query( SystemDictType.get_mini_fields(), fil,  SystemDictType.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemDictType:
        entity = SystemDictType()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemDictType:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemDictType=await self.GetExist(id)
        if entity.tenantId!=current_tenant_id.get():
            raise FriendlyException('不能操作系统默认数据')
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id:int):
        await self.DeleteWhere([SystemDictType.id==id])
    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemDictType.id.in_(ids)])
    async def GetByType(self,dictType:str)->SystemDictType:
        return await self.QueryOne([SystemDictType.type==dictType])
    async def GetByTypes(self,enumsFields)->List[SystemDictType]:
        return await self.QueryWhere([SystemDictType.type.in_(enumsFields),SystemDictType.deleted==0])