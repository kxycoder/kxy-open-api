import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.trade.models.trade_brokerage_user import TradeBrokerageUser
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class TradeBrokerageUserDal(MyBaseDal[TradeBrokerageUser]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(TradeBrokerageUser,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[TradeBrokerageUser]:
        return await self.QueryWhere([TradeBrokerageUser.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[TradeBrokerageUser],int]:
        fil = list()
        fil.append(TradeBrokerageUser.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeBrokerageUser,k) and v:
                fil.append(getattr(TradeBrokerageUser,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeBrokerageUser.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeBrokerageUser.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(TradeBrokerageUser.DicType.ilike("%" + search_text + "%"),
            #                  TradeBrokerageUser.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, TradeBrokerageUser.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[TradeBrokerageUser]:
        fil = list()
        fil.append( TradeBrokerageUser.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeBrokerageUser,k) and v:
                fil.append(getattr(TradeBrokerageUser,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( TradeBrokerageUser.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( TradeBrokerageUser. == int(status))
        items = await self.page_fields_nocount_query( TradeBrokerageUser.get_mini_fields(), fil,  TradeBrokerageUser.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->TradeBrokerageUser:
        entity = TradeBrokerageUser()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->TradeBrokerageUser:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeBrokerageUser=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([TradeBrokerageUser.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([TradeBrokerageUser.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[TradeBrokerageUser],int]:
        fil = list()
        fil.append(TradeBrokerageUser.creator == self.UserId)
        fil.append(TradeBrokerageUser.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeBrokerageUser.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeBrokerageUser.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, TradeBrokerageUser.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->TradeBrokerageUser:
        entity = TradeBrokerageUser()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->TradeBrokerageUser:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeBrokerageUser=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([TradeBrokerageUser.id==id,TradeBrokerageUser.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([TradeBrokerageUser.id.in_(ids),TradeBrokerageUser.creator==self.UserId])
