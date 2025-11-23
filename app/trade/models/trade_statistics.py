from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class TradeStatistics(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'trade_statistics'


    id = Column('id',Integer, comment='编号，主键自增',primary_key=True,autoincrement=True)
    time = Column('time',DateTime, comment='统计日期')
    orderCreateCount = Column('order_create_count',Integer, comment='创建订单数')
    orderPayCount = Column('order_pay_count',Integer, comment='支付订单商品数')
    orderPayPrice = Column('order_pay_price',Integer, comment='总支付金额，单位：分')
    afterSaleCount = Column('after_sale_count',Integer, comment='退款订单数')
    afterSaleRefundPrice = Column('after_sale_refund_price',Integer, comment='总退款金额，单位：分')
    brokerageSettlementPrice = Column('brokerage_settlement_price',Integer, comment='佣金金额（已结算），单位：分')
    walletPayPrice = Column('wallet_pay_price',Integer, comment='总支付金额（余额），单位：分')
    rechargePayCount = Column('recharge_pay_count',Integer, comment='充值订单数')
    rechargePayPrice = Column('recharge_pay_price',Integer, comment='充值金额，单位：分')
    rechargeRefundCount = Column('recharge_refund_count',Integer, comment='充值退款订单数')
    rechargeRefundPrice = Column('recharge_refund_price',Integer, comment='充值退款金额，单位：分')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')
    index = Column('INDEX',String(0), comment='INDEX')


    InsertRequireFields = ['time', 'orderCreateCount', 'orderPayCount', 'orderPayPrice', 'afterSaleCount', 'afterSaleRefundPrice', 'brokerageSettlementPrice', 'walletPayPrice', 'rechargePayCount', 'rechargePayPrice', 'rechargeRefundCount', 'rechargeRefundPrice']
    InsertOtherFields= ['index']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'time': self.time.strftime("%Y-%m-%d %H:%M:%S") if self.time else None,
           'orderCreateCount': self.orderCreateCount,
           'orderPayCount': self.orderPayCount,
           'orderPayPrice': self.orderPayPrice,
           'afterSaleCount': self.afterSaleCount,
           'afterSaleRefundPrice': self.afterSaleRefundPrice,
           'brokerageSettlementPrice': self.brokerageSettlementPrice,
           'walletPayPrice': self.walletPayPrice,
           'rechargePayCount': self.rechargePayCount,
           'rechargePayPrice': self.rechargePayPrice,
           'rechargeRefundCount': self.rechargeRefundCount,
           'rechargeRefundPrice': self.rechargeRefundPrice,
           'creator': self.creator,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updater': self.updater,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'deleted': self.deleted,
           'tenantId': self.tenantId,
           'index': self.index,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'time': self.time,
           'orderCreateCount': self.orderCreateCount,
           'orderPayCount': self.orderPayCount,
           'orderPayPrice': self.orderPayPrice,
           'afterSaleCount': self.afterSaleCount,
           'afterSaleRefundPrice': self.afterSaleRefundPrice,
           'brokerageSettlementPrice': self.brokerageSettlementPrice,
           'walletPayPrice': self.walletPayPrice,
           'rechargePayCount': self.rechargePayCount,
           'rechargePayPrice': self.rechargePayPrice,
           'rechargeRefundCount': self.rechargeRefundCount,
           'rechargeRefundPrice': self.rechargeRefundPrice,
           'index': self.index,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeStatistics.id,TradeStatistics.time,TradeStatistics.orderCreateCount,TradeStatistics.orderPayCount,TradeStatistics.orderPayPrice,TradeStatistics.afterSaleCount,TradeStatistics.afterSaleRefundPrice,TradeStatistics.brokerageSettlementPrice,TradeStatistics.walletPayPrice,TradeStatistics.rechargePayCount,TradeStatistics.rechargePayPrice,TradeStatistics.rechargeRefundCount,TradeStatistics.rechargeRefundPrice,TradeStatistics.index]