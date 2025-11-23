import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.trade.models.trade_delivery_express_template import TradeDeliveryExpressTemplate
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class TradeDeliveryExpressTemplateDal(MyBaseDal[TradeDeliveryExpressTemplate]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(TradeDeliveryExpressTemplate,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[TradeDeliveryExpressTemplate]:
        return await self.QueryWhere([TradeDeliveryExpressTemplate.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[TradeDeliveryExpressTemplate],int]:
        fil = list()
        fil.append(TradeDeliveryExpressTemplate.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeDeliveryExpressTemplate,k) and v:
                fil.append(getattr(TradeDeliveryExpressTemplate,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeDeliveryExpressTemplate.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeDeliveryExpressTemplate.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(TradeDeliveryExpressTemplate.DicType.ilike("%" + search_text + "%"),
            #                  TradeDeliveryExpressTemplate.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, TradeDeliveryExpressTemplate.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[TradeDeliveryExpressTemplate]:
        fil = list()
        fil.append( TradeDeliveryExpressTemplate.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeDeliveryExpressTemplate,k) and v:
                fil.append(getattr(TradeDeliveryExpressTemplate,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( TradeDeliveryExpressTemplate.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( TradeDeliveryExpressTemplate. == int(status))
        items = await self.page_fields_nocount_query( TradeDeliveryExpressTemplate.get_mini_fields(), fil,  TradeDeliveryExpressTemplate.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->TradeDeliveryExpressTemplate:
        entity = TradeDeliveryExpressTemplate()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->TradeDeliveryExpressTemplate:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeDeliveryExpressTemplate=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([TradeDeliveryExpressTemplate.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([TradeDeliveryExpressTemplate.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[TradeDeliveryExpressTemplate],int]:
        fil = list()
        fil.append(TradeDeliveryExpressTemplate.creator == self.UserId)
        fil.append(TradeDeliveryExpressTemplate.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeDeliveryExpressTemplate.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeDeliveryExpressTemplate.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, TradeDeliveryExpressTemplate.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->TradeDeliveryExpressTemplate:
        entity = TradeDeliveryExpressTemplate()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->TradeDeliveryExpressTemplate:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeDeliveryExpressTemplate=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([TradeDeliveryExpressTemplate.id==id,TradeDeliveryExpressTemplate.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([TradeDeliveryExpressTemplate.id.in_(ids),TradeDeliveryExpressTemplate.creator==self.UserId])
    async def GetAllSimpleList(self):
        return await self.QueryWhere([TradeDeliveryExpressTemplate.deleted == 0], TradeDeliveryExpressTemplate.get_mini_fields())