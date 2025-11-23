import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.pay.models.pay_demo_order import PayDemoOrder
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class PayDemoOrderDal(MyBaseDal[PayDemoOrder]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(PayDemoOrder,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[PayDemoOrder]:
        return await self.QueryWhere([PayDemoOrder.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[PayDemoOrder],int]:
        fil = list()
        fil.append(PayDemoOrder.deleted == 0)
        for k,v in search.items():
            if hasattr(PayDemoOrder,k) and v:
                fil.append(getattr(PayDemoOrder,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayDemoOrder.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayDemoOrder.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(PayDemoOrder.DicType.ilike("%" + search_text + "%"),
            #                  PayDemoOrder.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, PayDemoOrder.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[PayDemoOrder]:
        fil = list()
        fil.append( PayDemoOrder.deleted == 0)
        for k,v in search.items():
            if hasattr(PayDemoOrder,k) and v:
                fil.append(getattr(PayDemoOrder,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( PayDemoOrder.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( PayDemoOrder. == int(status))
        items = await self.page_fields_nocount_query( PayDemoOrder.get_mini_fields(), fil,  PayDemoOrder.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->PayDemoOrder:
        entity = PayDemoOrder()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->PayDemoOrder:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayDemoOrder=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([PayDemoOrder.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([PayDemoOrder.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[PayDemoOrder],int]:
        fil = list()
        fil.append(PayDemoOrder.userId == self.UserId)
        fil.append(PayDemoOrder.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayDemoOrder.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayDemoOrder.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, PayDemoOrder.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->PayDemoOrder:
        entity = PayDemoOrder()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.userId=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->PayDemoOrder:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayDemoOrder=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([PayDemoOrder.id==id,PayDemoOrder.userId==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([PayDemoOrder.id.in_(ids),PayDemoOrder.userId==self.UserId])
