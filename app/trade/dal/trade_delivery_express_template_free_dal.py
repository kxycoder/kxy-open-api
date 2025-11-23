import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.trade.models.trade_delivery_express_template_free import TradeDeliveryExpressTemplateFree
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class TradeDeliveryExpressTemplateFreeDal(MyBaseDal[TradeDeliveryExpressTemplateFree]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(TradeDeliveryExpressTemplateFree,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[TradeDeliveryExpressTemplateFree]:
        return await self.QueryWhere([TradeDeliveryExpressTemplateFree.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[TradeDeliveryExpressTemplateFree],int]:
        fil = list()
        fil.append(TradeDeliveryExpressTemplateFree.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeDeliveryExpressTemplateFree,k) and v:
                fil.append(getattr(TradeDeliveryExpressTemplateFree,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeDeliveryExpressTemplateFree.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeDeliveryExpressTemplateFree.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(TradeDeliveryExpressTemplateFree.DicType.ilike("%" + search_text + "%"),
            #                  TradeDeliveryExpressTemplateFree.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, TradeDeliveryExpressTemplateFree.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[TradeDeliveryExpressTemplateFree]:
        fil = list()
        fil.append( TradeDeliveryExpressTemplateFree.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeDeliveryExpressTemplateFree,k) and v:
                fil.append(getattr(TradeDeliveryExpressTemplateFree,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( TradeDeliveryExpressTemplateFree.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( TradeDeliveryExpressTemplateFree. == int(status))
        items = await self.page_fields_nocount_query( TradeDeliveryExpressTemplateFree.get_mini_fields(), fil,  TradeDeliveryExpressTemplateFree.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->TradeDeliveryExpressTemplateFree:
        entity = TradeDeliveryExpressTemplateFree()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->TradeDeliveryExpressTemplateFree:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeDeliveryExpressTemplateFree=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([TradeDeliveryExpressTemplateFree.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([TradeDeliveryExpressTemplateFree.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[TradeDeliveryExpressTemplateFree],int]:
        fil = list()
        fil.append(TradeDeliveryExpressTemplateFree.creator == self.UserId)
        fil.append(TradeDeliveryExpressTemplateFree.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeDeliveryExpressTemplateFree.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeDeliveryExpressTemplateFree.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, TradeDeliveryExpressTemplateFree.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->TradeDeliveryExpressTemplateFree:
        entity = TradeDeliveryExpressTemplateFree()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->TradeDeliveryExpressTemplateFree:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeDeliveryExpressTemplateFree=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([TradeDeliveryExpressTemplateFree.id==id,TradeDeliveryExpressTemplateFree.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([TradeDeliveryExpressTemplateFree.id.in_(ids),TradeDeliveryExpressTemplateFree.creator==self.UserId])

    async def GetByTemplateId(self, template_id: int) -> List[TradeDeliveryExpressTemplateFree]:
        """
        根据运费模板ID获取包邮规则列表
        :param template_id: 运费模板ID
        :return: 包邮规则列表
        """
        return await self.QueryWhere([
            TradeDeliveryExpressTemplateFree.templateId == template_id,
            TradeDeliveryExpressTemplateFree.deleted == 0
        ])

    async def DeleteByTemplateId(self, template_id: int):
        """
        根据运费模板ID删除包邮规则
        :param template_id: 运费模板ID
        """
        await self.DeleteWhere([TradeDeliveryExpressTemplateFree.templateId == template_id])
