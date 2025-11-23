import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.product.models.product_sku import ProductSku
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class ProductSkuDal(MyBaseDal[ProductSku]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(ProductSku,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[ProductSku]:
        return await self.QueryWhere([ProductSku.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[ProductSku],int]:
        fil = list()
        fil.append(ProductSku.deleted == 0)
        for k,v in search.items():
            if hasattr(ProductSku,k) and v:
                fil.append(getattr(ProductSku,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ProductSku.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ProductSku.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(ProductSku.DicType.ilike("%" + search_text + "%"),
            #                  ProductSku.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, ProductSku.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[ProductSku]:
        fil = list()
        fil.append( ProductSku.deleted == 0)
        for k,v in search.items():
            if hasattr(ProductSku,k) and v:
                fil.append(getattr(ProductSku,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( ProductSku.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( ProductSku. == int(status))
        items = await self.page_fields_nocount_query( ProductSku.get_mini_fields(), fil,  ProductSku.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->ProductSku:
        entity = ProductSku()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->ProductSku:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ProductSku=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([ProductSku.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([ProductSku.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[ProductSku],int]:
        fil = list()
        fil.append(ProductSku.creator == self.UserId)
        fil.append(ProductSku.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ProductSku.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ProductSku.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, ProductSku.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->ProductSku:
        entity = ProductSku()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->ProductSku:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ProductSku=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([ProductSku.id==id,ProductSku.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([ProductSku.id.in_(ids),ProductSku.creator==self.UserId])
    async def GetBySpuId(self,id):
        return await self.QueryWhere([ProductSku.spuId==id,ProductSku.deleted==0],fields=ProductSku.get_mini_fields())