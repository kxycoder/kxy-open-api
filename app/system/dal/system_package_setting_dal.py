import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_package_setting import SystemPackageSetting
from app.tools import utils


from app.common.basedal import MyBaseDal


class SystemPackageSettingDal(MyBaseDal[SystemPackageSetting]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemPackageSetting,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemPackageSetting],int]:
        fil = list()
        fil.append(SystemPackageSetting.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemPackageSetting,k) and v:
                fil.append(getattr(SystemPackageSetting,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemPackageSetting.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemPackageSetting.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemPackageSetting.DicType.ilike("%" + search_text + "%"),
            #                  SystemPackageSetting.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, SystemPackageSetting.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemPackageSetting]:
        fil = list()
        fil.append( SystemPackageSetting.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemPackageSetting,k) and v:
                fil.append(getattr(SystemPackageSetting,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemPackageSetting.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( SystemPackageSetting. == int(status))
        items = await self.page_fields_nocount_query( SystemPackageSetting.get_mini_fields(), fil,  SystemPackageSetting.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemPackageSetting:
        entity = SystemPackageSetting()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemPackageSetting:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemPackageSetting=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemPackageSetting.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemPackageSetting.id.in_(ids)])
 
    async def GetCategorySetting(self,categoryName,packageId):
        exist = await self.QueryOne([SystemPackageSetting.categoryName==categoryName,SystemPackageSetting.packageId==packageId],fields=[SystemPackageSetting.ids])
        if exist:
            return exist.ids
        return []