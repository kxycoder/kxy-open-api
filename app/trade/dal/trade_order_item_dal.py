import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.trade.models.trade_order_item import TradeOrderItem
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class TradeOrderItemDal(MyBaseDal[TradeOrderItem]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(TradeOrderItem,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[TradeOrderItem]:
        return await self.QueryWhere([TradeOrderItem.id.in_(ids)])

    async def GetByOrderIds(self,order_ids)->List[TradeOrderItem]:
        """根据订单ID列表查询订单明细"""
        return await self.QueryWhere([TradeOrderItem.orderId.in_(order_ids), TradeOrderItem.deleted == 0])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[TradeOrderItem],int]:
        fil = list()
        fil.append(TradeOrderItem.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeOrderItem,k) and v:
                fil.append(getattr(TradeOrderItem,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeOrderItem.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeOrderItem.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(TradeOrderItem.DicType.ilike("%" + search_text + "%"),
            #                  TradeOrderItem.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, TradeOrderItem.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[TradeOrderItem]:
        fil = list()
        fil.append( TradeOrderItem.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeOrderItem,k) and v:
                fil.append(getattr(TradeOrderItem,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( TradeOrderItem.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( TradeOrderItem. == int(status))
        items = await self.page_fields_nocount_query( TradeOrderItem.get_mini_fields(), fil,  TradeOrderItem.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->TradeOrderItem:
        entity = TradeOrderItem()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->TradeOrderItem:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeOrderItem=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([TradeOrderItem.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([TradeOrderItem.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[TradeOrderItem],int]:
        fil = list()
        fil.append(TradeOrderItem.userId == self.UserId)
        fil.append(TradeOrderItem.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeOrderItem.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeOrderItem.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, TradeOrderItem.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->TradeOrderItem:
        entity = TradeOrderItem()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.userId=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->TradeOrderItem:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeOrderItem=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([TradeOrderItem.id==id,TradeOrderItem.userId==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([TradeOrderItem.id.in_(ids),TradeOrderItem.userId==self.UserId])
