import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.trade.models.trade_brokerage_record import TradeBrokerageRecord
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class TradeBrokerageRecordDal(MyBaseDal[TradeBrokerageRecord]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(TradeBrokerageRecord,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[TradeBrokerageRecord]:
        return await self.QueryWhere([TradeBrokerageRecord.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[TradeBrokerageRecord],int]:
        fil = list()
        fil.append(TradeBrokerageRecord.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeBrokerageRecord,k) and v:
                fil.append(getattr(TradeBrokerageRecord,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeBrokerageRecord.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeBrokerageRecord.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(TradeBrokerageRecord.DicType.ilike("%" + search_text + "%"),
            #                  TradeBrokerageRecord.Description.ilike("%" + search_text + "%")))

        status = search.get('status')
        if status:
            fil.append(TradeBrokerageRecord.status == int(status))

        items, total_count = await self.paginate_query(fil, TradeBrokerageRecord.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[TradeBrokerageRecord]:
        fil = list()
        fil.append( TradeBrokerageRecord.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeBrokerageRecord,k) and v:
                fil.append(getattr(TradeBrokerageRecord,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( TradeBrokerageRecord.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( TradeBrokerageRecord.status == int(status))
        items = await self.page_fields_nocount_query( TradeBrokerageRecord.get_mini_fields(), fil,  TradeBrokerageRecord.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->TradeBrokerageRecord:
        entity = TradeBrokerageRecord()
        entity.InitInsertEntityWithJson(jsonData)
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->TradeBrokerageRecord:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeBrokerageRecord=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([TradeBrokerageRecord.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([TradeBrokerageRecord.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[TradeBrokerageRecord],int]:
        fil = list()
        fil.append(TradeBrokerageRecord.userId == self.UserId)
        fil.append(TradeBrokerageRecord.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeBrokerageRecord.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeBrokerageRecord.Name.ilike("%" + search_text + "%"))

        status = search.get('status')
        if status:
            fil.append(TradeBrokerageRecord.status == int(status))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, TradeBrokerageRecord.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->TradeBrokerageRecord:
        entity = TradeBrokerageRecord()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.userId=self.UserId
        

        entity.status = 0

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->TradeBrokerageRecord:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeBrokerageRecord=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([TradeBrokerageRecord.id==id,TradeBrokerageRecord.userId==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([TradeBrokerageRecord.id.in_(ids),TradeBrokerageRecord.userId==self.UserId])
