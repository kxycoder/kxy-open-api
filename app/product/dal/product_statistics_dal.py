import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.product.models.product_statistics import ProductStatistics
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class ProductStatisticsDal(MyBaseDal[ProductStatistics]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(ProductStatistics,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[ProductStatistics]:
        return await self.QueryWhere([ProductStatistics.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[ProductStatistics],int]:
        fil = list()
        fil.append(ProductStatistics.deleted == 0)
        for k,v in search.items():
            if hasattr(ProductStatistics,k) and v:
                fil.append(getattr(ProductStatistics,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ProductStatistics.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ProductStatistics.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(ProductStatistics.DicType.ilike("%" + search_text + "%"),
            #                  ProductStatistics.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, ProductStatistics.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[ProductStatistics]:
        fil = list()
        fil.append( ProductStatistics.deleted == 0)
        for k,v in search.items():
            if hasattr(ProductStatistics,k) and v:
                fil.append(getattr(ProductStatistics,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( ProductStatistics.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( ProductStatistics. == int(status))
        items = await self.page_fields_nocount_query( ProductStatistics.get_mini_fields(), fil,  ProductStatistics.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->ProductStatistics:
        entity = ProductStatistics()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->ProductStatistics:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ProductStatistics=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([ProductStatistics.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([ProductStatistics.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[ProductStatistics],int]:
        fil = list()
        fil.append(ProductStatistics.creator == self.UserId)
        fil.append(ProductStatistics.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ProductStatistics.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ProductStatistics.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, ProductStatistics.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->ProductStatistics:
        entity = ProductStatistics()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->ProductStatistics:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ProductStatistics=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([ProductStatistics.id==id,ProductStatistics.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([ProductStatistics.id.in_(ids),ProductStatistics.creator==self.UserId])
