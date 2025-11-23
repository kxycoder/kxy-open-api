import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.trade.models.trade_order import TradeOrder
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger
from app.trade.enums import OrderStatusEnum

class TradeOrderDal(MyBaseDal[TradeOrder]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(TradeOrder,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[TradeOrder]:
        return await self.QueryWhere([TradeOrder.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[TradeOrder],int]:
        fil = list()
        fil.append(TradeOrder.deleted == 0)

        # 订单编号精确查询
        no = search.get('no')
        if no:
            fil.append(TradeOrder.no == str(no))

        # 订单状态
        status = search.get('status')
        if status is not None and status != '':
            fil.append(TradeOrder.status == int(status))

        # 支付渠道代码
        payChannelCode = search.get('payChannelCode')
        if payChannelCode:
            fil.append(TradeOrder.payChannelCode == str(payChannelCode))

        # 订单来源终端
        terminal = search.get('terminal')
        if terminal is not None and terminal != '':
            fil.append(TradeOrder.terminal == int(terminal))

        # 订单类型
        order_type = search.get('type')
        if order_type is not None and order_type != '':
            fil.append(TradeOrder.type == int(order_type))

        # 配送类型
        deliveryType = search.get('deliveryType')
        if deliveryType is not None and deliveryType != '':
            fil.append(TradeOrder.deliveryType == int(deliveryType))

        # 物流公司编号
        logisticsId = search.get('logisticsId')
        if logisticsId is not None and logisticsId != '':
            fil.append(TradeOrder.logisticsId == int(logisticsId))

        # 创建时间范围查询
        createTime = search.get('createTime')
        if createTime and isinstance(createTime, list) and len(createTime) >= 2:
            start_time = createTime[0]
            end_time = createTime[1]
            if start_time:
                fil.append(TradeOrder.createTime >= start_time)
            if end_time:
                fil.append(TradeOrder.createTime <= end_time)

        # 用户编号
        userId = search.get('userId')
        if userId is not None and userId != '':
            fil.append(TradeOrder.userId == int(userId))

        # 支付状态
        payStatus = search.get('payStatus')
        if payStatus is not None and payStatus != '':
            fil.append(TradeOrder.payStatus == int(payStatus))

        # 评价状态
        commentStatus = search.get('commentStatus')
        if commentStatus is not None and commentStatus != '':
            fil.append(TradeOrder.commentStatus == int(commentStatus))

        # 售后状态
        refundStatus = search.get('refundStatus')
        if refundStatus is not None and refundStatus != '':
            fil.append(TradeOrder.refundStatus == int(refundStatus))

        # 自提门店编号
        pickUpStoreId = search.get('pickUpStoreId')
        if pickUpStoreId is not None and pickUpStoreId != '':
            fil.append(TradeOrder.pickUpStoreId == int(pickUpStoreId))

        # 收件人手机号
        userMobile = search.get('userMobile')
        if userMobile:
            fil.append(TradeOrder.receiverMobile==userMobile)
            
        # 收件人姓名
        userNickname = search.get('userNickname')
        if userNickname:
            fil.append(TradeOrder.receiverName.ilike(f"%{userNickname}%"))

        items, total_count = await self.paginate_query(fil, TradeOrder.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[TradeOrder]:
        fil = list()
        fil.append( TradeOrder.deleted == 0)
        for k,v in search.items():
            if hasattr(TradeOrder,k) and v:
                fil.append(getattr(TradeOrder,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( TradeOrder.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( TradeOrder.status == int(status))
        items = await self.page_fields_nocount_query( TradeOrder.get_mini_fields(), fil,  TradeOrder.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->TradeOrder:
        entity = TradeOrder()
        entity.InitInsertEntityWithJson(jsonData)
        entity.status = int(OrderStatusEnum.UNPAID)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->TradeOrder:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeOrder=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([TradeOrder.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([TradeOrder.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[TradeOrder],int]:
        fil = list()
        fil.append(TradeOrder.userId == self.UserId)
        fil.append(TradeOrder.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(TradeOrder.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(TradeOrder.Name.ilike("%" + search_text + "%"))

        status = search.get('status')
        if status:
            fil.append(TradeOrder.status == int(status))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, TradeOrder.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->TradeOrder:
        entity = TradeOrder()
        entity.InitInsertEntityWithJson(jsonData)

        entity.userId=self.UserId


        entity.status = int(OrderStatusEnum.UNPAID)

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->TradeOrder:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:TradeOrder=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([TradeOrder.id==id,TradeOrder.userId==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([TradeOrder.id.in_(ids),TradeOrder.userId==self.UserId])
