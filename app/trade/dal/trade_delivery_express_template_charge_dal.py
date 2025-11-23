import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.trade.models.trade_delivery_express_template_charge import TradeDeliveryExpressTemplateCharge
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class TradeDeliveryExpressTemplateChargeDal(MyBaseDal[TradeDeliveryExpressTemplateCharge]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(TradeDeliveryExpressTemplateCharge,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[TradeDeliveryExpressTemplateCharge]:
        return await self.QueryWhere([TradeDeliveryExpressTemplateCharge.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[TradeDeliveryExpressTemplateCharge],int]:
        fil = list()
        fil.append(TradeDeliveryExpressTemplateCharge.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeDeliveryExpressTemplateCharge,k) and v:
                fil.append(getattr(TradeDeliveryExpressTemplateCharge,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeDeliveryExpressTemplateCharge.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeDeliveryExpressTemplateCharge.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(TradeDeliveryExpressTemplateCharge.DicType.ilike("%" + search_text + "%"),
            #                  TradeDeliveryExpressTemplateCharge.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, TradeDeliveryExpressTemplateCharge.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[TradeDeliveryExpressTemplateCharge]:
        fil = list()
        fil.append( TradeDeliveryExpressTemplateCharge.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeDeliveryExpressTemplateCharge,k) and v:
                fil.append(getattr(TradeDeliveryExpressTemplateCharge,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( TradeDeliveryExpressTemplateCharge.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( TradeDeliveryExpressTemplateCharge. == int(status))
        items = await self.page_fields_nocount_query( TradeDeliveryExpressTemplateCharge.get_mini_fields(), fil,  TradeDeliveryExpressTemplateCharge.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->TradeDeliveryExpressTemplateCharge:
        entity = TradeDeliveryExpressTemplateCharge()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->TradeDeliveryExpressTemplateCharge:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeDeliveryExpressTemplateCharge=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([TradeDeliveryExpressTemplateCharge.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([TradeDeliveryExpressTemplateCharge.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[TradeDeliveryExpressTemplateCharge],int]:
        fil = list()
        fil.append(TradeDeliveryExpressTemplateCharge.creator == self.UserId)
        fil.append(TradeDeliveryExpressTemplateCharge.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeDeliveryExpressTemplateCharge.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeDeliveryExpressTemplateCharge.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, TradeDeliveryExpressTemplateCharge.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->TradeDeliveryExpressTemplateCharge:
        entity = TradeDeliveryExpressTemplateCharge()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->TradeDeliveryExpressTemplateCharge:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeDeliveryExpressTemplateCharge=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([TradeDeliveryExpressTemplateCharge.id==id,TradeDeliveryExpressTemplateCharge.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([TradeDeliveryExpressTemplateCharge.id.in_(ids),TradeDeliveryExpressTemplateCharge.creator==self.UserId])

    async def GetByTemplateId(self, template_id: int) -> List[TradeDeliveryExpressTemplateCharge]:
        """
        根据运费模板ID获取计费规则列表
        :param template_id: 运费模板ID
        :return: 计费规则列表
        """
        return await self.QueryWhere([
            TradeDeliveryExpressTemplateCharge.templateId == template_id,
            TradeDeliveryExpressTemplateCharge.deleted == 0
        ])

    async def DeleteByTemplateId(self, template_id: int):
        """
        根据运费模板ID删除计费规则
        :param template_id: 运费模板ID
        """
        await self.DeleteWhere([TradeDeliveryExpressTemplateCharge.templateId == template_id])
