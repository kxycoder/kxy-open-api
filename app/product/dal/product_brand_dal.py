import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.product.models.product_brand import ProductBrand
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class ProductBrandDal(MyBaseDal[ProductBrand]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(ProductBrand,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[ProductBrand]:
        return await self.QueryWhere([ProductBrand.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[ProductBrand],int]:
        fil = list()
        fil.append(ProductBrand.deleted == 0)
        for k,v in search.items():
            if hasattr(ProductBrand,k) and v:
                fil.append(getattr(ProductBrand,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ProductBrand.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ProductBrand.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(ProductBrand.DicType.ilike("%" + search_text + "%"),
            #                  ProductBrand.Description.ilike("%" + search_text + "%")))

        status = search.get('status')
        if status:
            fil.append(ProductBrand.status == int(status))

        items, total_count = await self.paginate_query(fil, ProductBrand.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[ProductBrand]:
        fil = list()
        fil.append( ProductBrand.deleted == 0)
        for k,v in search.items():
            if hasattr(ProductBrand,k) and v:
                fil.append(getattr(ProductBrand,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( ProductBrand.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( ProductBrand.status == int(status))
        items = await self.page_fields_nocount_query( ProductBrand.get_mini_fields(), fil,  ProductBrand.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->ProductBrand:
        entity = ProductBrand()
        entity.InitInsertEntityWithJson(jsonData)
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->ProductBrand:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ProductBrand=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([ProductBrand.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([ProductBrand.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[ProductBrand],int]:
        fil = list()
        fil.append(ProductBrand.creator == self.UserId)
        fil.append(ProductBrand.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ProductBrand.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ProductBrand.Name.ilike("%" + search_text + "%"))

        status = search.get('status')
        if status:
            fil.append(ProductBrand.status == int(status))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, ProductBrand.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->ProductBrand:
        entity = ProductBrand()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.status = 0

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->ProductBrand:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ProductBrand=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([ProductBrand.id==id,ProductBrand.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([ProductBrand.id.in_(ids),ProductBrand.creator==self.UserId])
    async def GetAllSimpleList(self):
        return await self.QueryWhere([ProductBrand.deleted == 0],fields=ProductBrand.get_mini_fields())