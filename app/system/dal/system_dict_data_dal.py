import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_dict_data import SystemDictData
from app.tools import utils
from kxy.framework.filter import ignore_filter
from kxy.framework.context import current_tenant_id
from app.common.basedal import MyBaseDal

class SystemDictDataDal(MyBaseDal[SystemDictData]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemDictData,session,**kwargs)
    # def _check_extend_field(self, field_name,value):
    #     if field_name!='tenantId':
    #         return super()._check_extend_field(field_name,value)
    #     return SystemDictData.tenantId.in_([1,current_tenant_id.get()])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemDictData],int]:
        fil = list()
        fil.append(SystemDictData.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemDictData,k) and v:
                fil.append(getattr(SystemDictData,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemDictData.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemDictData.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemDictData.DicType.ilike("%" + search_text + "%"),
            #                  SystemDictData.Description.ilike("%" + search_text + "%")))
        status = search.get('status')

        if status:
            fil.append(SystemDictData.status == int(status))
        items, total_count = await self.paginate_query(fil, SystemDictData.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemDictData],int]:
        fil = list()
        fil.append(SystemDictData.UID == self.UserId)
        fil.append(SystemDictData.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemDictData.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemDictData.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemDictData.status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemDictData.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,)->List[SystemDictData]:
        fil = list()
        fil.append(SystemDictData.deleted == 0)
        items = await self.QueryWhere(fil,[SystemDictData.label,SystemDictData.value,SystemDictData.dictType,SystemDictData.colorType,SystemDictData.cssClass],orderBy=SystemDictData.sort.asc())
        return items

    async def AddByJsonData(self, jsonData)->SystemDictData:
        entity = SystemDictData()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemDictData:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemDictData=await self.GetExist(id)
        if entity.tenantId!=current_tenant_id.get():
            raise FriendlyException('不能操作系统默认数据')
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemDictData.id==id])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemDictData.id.in_(ids)])

    async def DeleteByType(self,type):
        return await self.DeleteWhere([SystemDictData.dictType==type])

    async def Get(self,id:int)->SystemDictData:
        return await self.QueryOne([SystemDictData.id==id])

    async def GetByType(self,type:str)->List[SystemDictData]:
        return await self.QueryWhere([SystemDictData.dictType==type,SystemDictData.deleted==0])
    
    async def GetByTypes(self,dictTypes):
        return await self.QueryWhere([SystemDictData.dictType.in_(dictTypes),SystemDictData.deleted==0])