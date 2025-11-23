from kxy.framework.base_service import BaseService
from kxy.framework.friendly_exception import FriendlyException
from datetime import datetime

from app.trade.dal.trade_order_dal import TradeOrderDal
from app.trade.dal.trade_order_item_dal import TradeOrderItemDal
from app.trade.dal.trade_order_log_dal import TradeOrderLogDal
from app.trade.dal.trade_delivery_express_dal import TradeDeliveryExpressDal
from app.member.dal.member_user_dal import MemberUserDal
from app.trade.enums import OrderStatusEnum, OrderOperateTypeEnum, UserTypeEnum

class OrderService(BaseService):
    async def GetOrderList(self, search, PageIndex, PageLimit):
        dal = TradeOrderDal(self.session)
        datas,total = await dal.Search(search, PageIndex, PageLimit)

        # 查询订单明细
        if datas:
            order_ids = [order.id for order in datas]
            item_dal = TradeOrderItemDal(self.session)
            items = await item_dal.GetByOrderIds(order_ids)

            # 将明细分组并填充到订单的items属性
            items_dict = {}
            for item in items:
                if item.orderId not in items_dict:
                    items_dict[item.orderId] = []
                items_dict[item.orderId].append(item)

            for order in datas:
                order.items = items_dict.get(order.id, [])

        return datas,total

    async def GetOrderDetail(self, order_id: int):
        # 查询订单基本信息
        dal = TradeOrderDal(self.session)
        order = await dal.GetExist(order_id)

        # 查询订单明细
        item_dal = TradeOrderItemDal(self.session)
        items = await item_dal.GetByOrderIds([order_id])
        order.items = items

        # 查询用户信息
        if order.userId:
            user_dal = MemberUserDal(self.session)
            try:
                user = await user_dal.GetSimpleUser(order.userId)
                order.user = user
            except:
                order.user = None
        else:
            order.user = None

        # 查询订单日志
        log_dal = TradeOrderLogDal(self.session)
        logs = await log_dal.GetByOrderId(order_id)
        order.logs = logs

        return order

    async def DeliveryOrder(self, order_id: int, logistics_id: int, logistics_no: str, admin_user: str = None):
        """
        订单发货
        :param order_id: 订单ID
        :param logistics_id: 物流公司编号
        :param logistics_no: 物流单号
        :param admin_user: 操作管理员
        :return: 更新后的订单
        """
        # 查询订单
        dal = TradeOrderDal(self.session)
        order = await dal.GetExist(order_id)

        # 校验订单状态 - 只有已支付的订单才能发货
        if not order.payStatus:
            raise FriendlyException('订单未支付,无法发货')

        # 校验订单状态 - 只有待发货状态的订单才能发货
        if order.status != OrderStatusEnum.UNDELIVERED:
            raise FriendlyException(f'订单状态不正确(当前状态:{OrderStatusEnum.get_desc(order.status)}),无法发货')

        # 查询物流公司信息
        express_dal = TradeDeliveryExpressDal(self.session)
        express = await express_dal.Get(logistics_id)
        logistics_name = express.name if express else f'物流公司ID:{logistics_id}'

        # 记录操作前状态
        before_status = order.status

        # 更新订单信息
        order.logisticsId = logistics_id
        order.logisticsNo = logistics_no
        order.deliveryTime = datetime.now()
        order.status = int(OrderStatusEnum.DELIVERED)
        order.updater = admin_user

        await dal.Update(order)

        # 记录订单日志
        log_dal = TradeOrderLogDal(self.session)
        log = await log_dal.AddByJsonData({
            'userId': order.userId,
            'userType': int(UserTypeEnum.ADMIN),
            'orderId': order_id,
            'beforeStatus': before_status,
            'afterStatus': int(OrderStatusEnum.DELIVERED),
            'operateType': int(OrderOperateTypeEnum.DELIVERY),
            'content': f'订单已发货，物流公司：{logistics_name}，物流单号：{logistics_no}'
        })

        return order