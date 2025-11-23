import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.trade.models.trade_after_sale_log import TradeAfterSaleLog
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class TradeAfterSaleLogDal(MyBaseDal[TradeAfterSaleLog]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(TradeAfterSaleLog,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[TradeAfterSaleLog]:
        return await self.QueryWhere([TradeAfterSaleLog.id.in_(ids)])

    async def GetByAfterSaleId(self, after_sale_id: int)->List[TradeAfterSaleLog]:
        """根据售后单ID查询售后日志"""
        fil = [
            TradeAfterSaleLog.afterSaleId == after_sale_id,
            TradeAfterSaleLog.deleted == 0
        ]
        return await self.QueryWhere(fil)
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[TradeAfterSaleLog],int]:
        fil = list()
        fil.append(TradeAfterSaleLog.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeAfterSaleLog,k) and v:
                fil.append(getattr(TradeAfterSaleLog,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeAfterSaleLog.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeAfterSaleLog.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(TradeAfterSaleLog.DicType.ilike("%" + search_text + "%"),
            #                  TradeAfterSaleLog.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, TradeAfterSaleLog.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[TradeAfterSaleLog]:
        fil = list()
        fil.append( TradeAfterSaleLog.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeAfterSaleLog,k) and v:
                fil.append(getattr(TradeAfterSaleLog,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( TradeAfterSaleLog.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( TradeAfterSaleLog. == int(status))
        items = await self.page_fields_nocount_query( TradeAfterSaleLog.get_mini_fields(), fil,  TradeAfterSaleLog.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->TradeAfterSaleLog:
        entity = TradeAfterSaleLog()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->TradeAfterSaleLog:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeAfterSaleLog=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([TradeAfterSaleLog.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([TradeAfterSaleLog.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[TradeAfterSaleLog],int]:
        fil = list()
        fil.append(TradeAfterSaleLog.userId == self.UserId)
        fil.append(TradeAfterSaleLog.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeAfterSaleLog.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeAfterSaleLog.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, TradeAfterSaleLog.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->TradeAfterSaleLog:
        entity = TradeAfterSaleLog()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.userId=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->TradeAfterSaleLog:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeAfterSaleLog=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([TradeAfterSaleLog.id==id,TradeAfterSaleLog.userId==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([TradeAfterSaleLog.id.in_(ids),TradeAfterSaleLog.userId==self.UserId])
