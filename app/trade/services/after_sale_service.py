from kxy.framework.base_service import BaseService
from kxy.framework.friendly_exception import FriendlyException

from app.trade.dal.trade_after_sale_dal import TradeAfterSaleDal
from app.trade.dal.trade_order_dal import TradeOrderDal
from app.trade.dal.trade_order_item_dal import TradeOrderItemDal
from app.trade.dal.trade_after_sale_log_dal import TradeAfterSaleLogDal
from app.member.dal.member_user_dal import MemberUserDal

class AfterSaleService(BaseService):
    async def GetAfterSaleDetail(self, after_sale_id: int):
        """
        查询售后单详情,包括关联的订单、订单项、用户和日志信息
        :param after_sale_id: 售后单ID
        :return: 售后单详情对象
        """
        # 查询售后单基本信息
        after_sale_dal = TradeAfterSaleDal(self.session)
        after_sale = await after_sale_dal.GetExist(after_sale_id)

        # 查询原始订单信息
        if after_sale.orderId:
            order_dal = TradeOrderDal(self.session)
            try:
                order = await order_dal.Get(after_sale.orderId)
                after_sale.order = order
            except:
                after_sale.order = None
        else:
            after_sale.order = None

        # 查询要退货的商品信息(订单项)
        if after_sale.orderItemId:
            order_item_dal = TradeOrderItemDal(self.session)
            try:
                order_item = await order_item_dal.Get(after_sale.orderItemId)
                after_sale.orderItem = order_item
            except:
                after_sale.orderItem = None
        else:
            after_sale.orderItem = None

        # 查询用户信息
        if after_sale.userId:
            user_dal = MemberUserDal(self.session)
            try:
                user = await user_dal.GetSimpleUser(after_sale.userId)
                after_sale.user = user
            except:
                after_sale.user = None
        else:
            after_sale.user = None

        # 查询售后日志
        log_dal = TradeAfterSaleLogDal(self.session)
        logs = await log_dal.GetByAfterSaleId(after_sale_id)
        after_sale.logs = logs

        return after_sale
