import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.trade.models.trade_order_log import TradeOrderLog
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class TradeOrderLogDal(MyBaseDal[TradeOrderLog]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(TradeOrderLog,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[TradeOrderLog]:
        return await self.QueryWhere([TradeOrderLog.id.in_(ids)])

    async def GetByOrderId(self, order_id: int)->List[TradeOrderLog]:
        """根据订单ID查询订单日志"""
        fil = [
            TradeOrderLog.orderId == order_id,
            TradeOrderLog.deleted == 0
        ]
        return await self.QueryWhere(fil)
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[TradeOrderLog],int]:
        fil = list()
        fil.append(TradeOrderLog.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeOrderLog,k) and v:
                fil.append(getattr(TradeOrderLog,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeOrderLog.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeOrderLog.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(TradeOrderLog.DicType.ilike("%" + search_text + "%"),
            #                  TradeOrderLog.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, TradeOrderLog.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[TradeOrderLog]:
        fil = list()
        fil.append( TradeOrderLog.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeOrderLog,k) and v:
                fil.append(getattr(TradeOrderLog,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( TradeOrderLog.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( TradeOrderLog. == int(status))
        items = await self.page_fields_nocount_query( TradeOrderLog.get_mini_fields(), fil,  TradeOrderLog.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->TradeOrderLog:
        entity = TradeOrderLog()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->TradeOrderLog:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeOrderLog=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([TradeOrderLog.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([TradeOrderLog.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[TradeOrderLog],int]:
        fil = list()
        fil.append(TradeOrderLog.userId == self.UserId)
        fil.append(TradeOrderLog.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeOrderLog.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeOrderLog.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, TradeOrderLog.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->TradeOrderLog:
        entity = TradeOrderLog()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.userId=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->TradeOrderLog:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeOrderLog=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([TradeOrderLog.id==id,TradeOrderLog.userId==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([TradeOrderLog.id.in_(ids),TradeOrderLog.userId==self.UserId])
