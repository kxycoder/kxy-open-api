import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.product.models.product_spu import ProductSpu
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class ProductSpuDal(MyBaseDal[ProductSpu]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(ProductSpu,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[ProductSpu]:
        return await self.QueryWhere([ProductSpu.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[ProductSpu],int]:
        fil = list()
        fil.append(ProductSpu.deleted == 0)
        for k,v in search.items():
            if hasattr(ProductSpu,k) and v:
                fil.append(getattr(ProductSpu,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search.get('tabType'):
            fil.append(ProductSpu.status == int(search.get('tabType')))
        if search.get('categoryId'):
            fil.append(ProductSpu.categoryId == int(search.get('categoryId')))
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ProductSpu.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ProductSpu.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(ProductSpu.DicType.ilike("%" + search_text + "%"),
            #                  ProductSpu.Description.ilike("%" + search_text + "%")))

        status = search.get('status')
        if status:
            fil.append(ProductSpu.status == int(status))

        items, total_count = await self.paginate_query(fil, ProductSpu.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[ProductSpu]:
        fil = list()
        fil.append( ProductSpu.deleted == 0)
        for k,v in search.items():
            if hasattr(ProductSpu,k) and v:
                fil.append(getattr(ProductSpu,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( ProductSpu.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( ProductSpu.status == int(status))
        items = await self.page_fields_nocount_query( ProductSpu.get_mini_fields(), fil,  ProductSpu.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->ProductSpu:
        entity = ProductSpu()
        entity.InitInsertEntityWithJson(jsonData)
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->ProductSpu:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ProductSpu=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([ProductSpu.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([ProductSpu.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[ProductSpu],int]:
        fil = list()
        fil.append(ProductSpu.creator == self.UserId)
        fil.append(ProductSpu.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ProductSpu.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ProductSpu.Name.ilike("%" + search_text + "%"))

        status = search.get('status')
        if status:
            fil.append(ProductSpu.status == int(status))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, ProductSpu.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->ProductSpu:
        entity = ProductSpu()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.status = 0

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->ProductSpu:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ProductSpu=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([ProductSpu.id==id,ProductSpu.creator==self.UserId])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([ProductSpu.id.in_(ids),ProductSpu.creator==self.UserId])

    async def GetCount(self):
        """
        统计每种状态的数量
        返回格式: {"0":6,"1":1,"2":1,"3":4,"4":0}
        """
        from sqlalchemy import func, case
        
        # 查询各个状态的数量
        status_counts = await self.session.execute(
            select(
                ProductSpu.status,
                func.count(ProductSpu.id).label('count')
            )
            .where(ProductSpu.deleted == 0)
            .group_by(ProductSpu.status)
        )
        
        # 将查询结果转换为字典
        count_dict = {str(row.status): row.count for row in status_counts.fetchall()}
        
        # 确保返回所有需要的状态（0-4），缺失的状态设为0
        result = {}
        for status in range(5):
            status_str = str(status)
            result[status_str] = count_dict.get(status_str, 0)
        
        return result