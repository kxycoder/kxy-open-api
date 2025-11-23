import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_package_category import SystemPackageCategory
from app.tools import utils


from app.common.basedal import MyBaseDal


class SystemPackageCategoryDal(MyBaseDal[SystemPackageCategory]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemPackageCategory,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemPackageCategory],int]:
        fil = list()
        fil.append(SystemPackageCategory.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemPackageCategory,k) and v:
                fil.append(getattr(SystemPackageCategory,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemPackageCategory.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemPackageCategory.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemPackageCategory.DicType.ilike("%" + search_text + "%"),
            #                  SystemPackageCategory.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, SystemPackageCategory.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemPackageCategory]:
        fil = list()
        fil.append( SystemPackageCategory.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemPackageCategory,k) and v:
                fil.append(getattr(SystemPackageCategory,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemPackageCategory.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( SystemPackageCategory. == int(status))
        items = await self.page_fields_nocount_query( SystemPackageCategory.get_mini_fields(), fil,  SystemPackageCategory.createTime.desc(), page_index, page_size)
        return items
    def checkPackageCategory(self,entity:SystemPackageCategory):
        model_class = utils.loadClass(entity.tableModel)

        # 判断类中是否存在 tenantId 属性
        if not hasattr(model_class, 'tenantId'):
            raise FriendlyException(f"类 {entity.tableModel} 中不存在 tenantId 属性")
    async def AddByJsonData(self, jsonData)->SystemPackageCategory:
        entity = SystemPackageCategory()
        entity.InitInsertEntityWithJson(jsonData)
        # self.checkPackageCategory(entity)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemPackageCategory:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemPackageCategory=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        # self.checkPackageCategory(entity)
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemPackageCategory.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemPackageCategory.id.in_(ids)])
 
    async def GetByName(self,categoryName)->SystemPackageCategory:
        return await self.QueryOne([SystemPackageCategory.name==categoryName,SystemPackageCategory.deleted==0])