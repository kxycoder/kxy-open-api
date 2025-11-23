import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.product.models.product_favorite import ProductFavorite
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class ProductFavoriteDal(MyBaseDal[ProductFavorite]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(ProductFavorite,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[ProductFavorite]:
        return await self.QueryWhere([ProductFavorite.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[ProductFavorite],int]:
        fil = list()
        fil.append(ProductFavorite.deleted == 0)
        for k,v in search.items():
            if hasattr(ProductFavorite,k) and v:
                fil.append(getattr(ProductFavorite,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ProductFavorite.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ProductFavorite.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(ProductFavorite.DicType.ilike("%" + search_text + "%"),
            #                  ProductFavorite.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, ProductFavorite.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[ProductFavorite]:
        fil = list()
        fil.append( ProductFavorite.deleted == 0)
        for k,v in search.items():
            if hasattr(ProductFavorite,k) and v:
                fil.append(getattr(ProductFavorite,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( ProductFavorite.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( ProductFavorite. == int(status))
        items = await self.page_fields_nocount_query( ProductFavorite.get_mini_fields(), fil,  ProductFavorite.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->ProductFavorite:
        entity = ProductFavorite()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->ProductFavorite:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ProductFavorite=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([ProductFavorite.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([ProductFavorite.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[ProductFavorite],int]:
        fil = list()
        fil.append(ProductFavorite.userId == self.UserId)
        fil.append(ProductFavorite.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ProductFavorite.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ProductFavorite.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, ProductFavorite.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->ProductFavorite:
        entity = ProductFavorite()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.userId=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->ProductFavorite:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ProductFavorite=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([ProductFavorite.id==id,ProductFavorite.userId==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([ProductFavorite.id.in_(ids),ProductFavorite.userId==self.UserId])
