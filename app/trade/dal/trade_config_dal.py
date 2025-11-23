import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.trade.models.trade_config import TradeConfig
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class TradeConfigDal(MyBaseDal[TradeConfig]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(TradeConfig,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[TradeConfig]:
        return await self.QueryWhere([TradeConfig.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[TradeConfig],int]:
        fil = list()
        fil.append(TradeConfig.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeConfig,k) and v:
                fil.append(getattr(TradeConfig,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeConfig.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeConfig.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(TradeConfig.DicType.ilike("%" + search_text + "%"),
            #                  TradeConfig.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, TradeConfig.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[TradeConfig]:
        fil = list()
        fil.append( TradeConfig.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeConfig,k) and v:
                fil.append(getattr(TradeConfig,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( TradeConfig.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( TradeConfig. == int(status))
        items = await self.page_fields_nocount_query( TradeConfig.get_mini_fields(), fil,  TradeConfig.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->TradeConfig:
        entity = TradeConfig()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->TradeConfig:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeConfig=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([TradeConfig.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([TradeConfig.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[TradeConfig],int]:
        fil = list()
        fil.append(TradeConfig.creator == self.UserId)
        fil.append(TradeConfig.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeConfig.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeConfig.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, TradeConfig.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->TradeConfig:
        entity = TradeConfig()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->TradeConfig:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeConfig=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([TradeConfig.id==id,TradeConfig.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([TradeConfig.id.in_(ids),TradeConfig.creator==self.UserId])
