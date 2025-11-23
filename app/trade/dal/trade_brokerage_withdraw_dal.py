import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.trade.models.trade_brokerage_withdraw import TradeBrokerageWithdraw
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class TradeBrokerageWithdrawDal(MyBaseDal[TradeBrokerageWithdraw]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(TradeBrokerageWithdraw,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[TradeBrokerageWithdraw]:
        return await self.QueryWhere([TradeBrokerageWithdraw.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[TradeBrokerageWithdraw],int]:
        fil = list()
        fil.append(TradeBrokerageWithdraw.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeBrokerageWithdraw,k) and v:
                fil.append(getattr(TradeBrokerageWithdraw,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeBrokerageWithdraw.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeBrokerageWithdraw.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(TradeBrokerageWithdraw.DicType.ilike("%" + search_text + "%"),
            #                  TradeBrokerageWithdraw.Description.ilike("%" + search_text + "%")))

        status = search.get('status')
        if status:
            fil.append(TradeBrokerageWithdraw.status == int(status))

        items, total_count = await self.paginate_query(fil, TradeBrokerageWithdraw.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[TradeBrokerageWithdraw]:
        fil = list()
        fil.append( TradeBrokerageWithdraw.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeBrokerageWithdraw,k) and v:
                fil.append(getattr(TradeBrokerageWithdraw,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( TradeBrokerageWithdraw.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( TradeBrokerageWithdraw.status == int(status))
        items = await self.page_fields_nocount_query( TradeBrokerageWithdraw.get_mini_fields(), fil,  TradeBrokerageWithdraw.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->TradeBrokerageWithdraw:
        entity = TradeBrokerageWithdraw()
        entity.InitInsertEntityWithJson(jsonData)
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->TradeBrokerageWithdraw:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeBrokerageWithdraw=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([TradeBrokerageWithdraw.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([TradeBrokerageWithdraw.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[TradeBrokerageWithdraw],int]:
        fil = list()
        fil.append(TradeBrokerageWithdraw.userId == self.UserId)
        fil.append(TradeBrokerageWithdraw.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeBrokerageWithdraw.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeBrokerageWithdraw.Name.ilike("%" + search_text + "%"))

        status = search.get('status')
        if status:
            fil.append(TradeBrokerageWithdraw.status == int(status))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, TradeBrokerageWithdraw.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->TradeBrokerageWithdraw:
        entity = TradeBrokerageWithdraw()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.userId=self.UserId
        

        entity.status = 0

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->TradeBrokerageWithdraw:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeBrokerageWithdraw=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([TradeBrokerageWithdraw.id==id,TradeBrokerageWithdraw.userId==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([TradeBrokerageWithdraw.id.in_(ids),TradeBrokerageWithdraw.userId==self.UserId])
