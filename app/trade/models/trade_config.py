from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger,Boolean
from kxy.framework.filter_tenant import FilterTenant
from kxy.framework.base_entity import JSONString

@FilterTenant()
class TradeConfig(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'trade_config'


    id = Column('id',Integer, comment='自增主键',primary_key=True,autoincrement=True)
    afterSaleRefundReasons = Column('after_sale_refund_reasons',JSONString(512), comment='售后退款理由')
    afterSaleReturnReasons = Column('after_sale_return_reasons',JSONString(512), comment='售后退货理由')
    deliveryExpressFreeEnabled = Column('delivery_express_free_enabled',Boolean, comment='是否启用全场包邮')
    deliveryExpressFreePrice = Column('delivery_express_free_price',Integer, comment='全场包邮的最小金额，单位：分')
    deliveryPickUpEnabled = Column('delivery_pick_up_enabled',Boolean, comment='是否开启自提')
    brokerageEnabled = Column('brokerage_enabled',Boolean, comment='是否启用分佣')
    brokerageEnabledCondition = Column('brokerage_enabled_condition',Integer, comment='分佣模式：1-人人分销 2-指定分销')
    brokerageBindMode = Column('brokerage_bind_mode',Integer, comment='分销关系绑定模式: 1-没有推广人，2-新用户, 3-扫码覆盖')
    brokeragePosterUrls = Column('brokerage_poster_urls',JSONString(2000), comment='分销海报图地址数组')
    brokerageFirstPercent = Column('brokerage_first_percent',Integer, comment='一级返佣比例')
    brokerageSecondPercent = Column('brokerage_second_percent',Integer, comment='二级返佣比例')
    brokerageWithdrawMinPrice = Column('brokerage_withdraw_min_price',Integer, comment='用户提现最低金额')
    brokerageWithdrawFeePercent = Column('brokerage_withdraw_fee_percent',Integer, comment='提现手续费百分比')
    brokerageFrozenDays = Column('brokerage_frozen_days',Integer, comment='佣金冻结时间(天)')
    brokerageWithdrawTypes = Column('brokerage_withdraw_types',JSONString(32), comment='提现方式：1-钱包；2-银行卡；3-微信；4-支付宝')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['deliveryExpressFreeEnabled', 'deliveryExpressFreePrice', 'deliveryPickUpEnabled', 'brokerageEnabled', 'brokerageEnabledCondition', 'brokerageBindMode', 'brokerageFirstPercent', 'brokerageSecondPercent', 'brokerageWithdrawMinPrice', 'brokerageWithdrawFeePercent', 'brokerageFrozenDays']
    InsertOtherFields= ['afterSaleRefundReasons', 'afterSaleReturnReasons', 'brokeragePosterUrls', 'brokerageWithdrawTypes']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'afterSaleRefundReasons': self.afterSaleRefundReasons,
           'afterSaleReturnReasons': self.afterSaleReturnReasons,
           'deliveryExpressFreeEnabled': self.deliveryExpressFreeEnabled,
           'deliveryExpressFreePrice': self.deliveryExpressFreePrice,
           'deliveryPickUpEnabled': self.deliveryPickUpEnabled,
           'brokerageEnabled': self.brokerageEnabled,
           'brokerageEnabledCondition': self.brokerageEnabledCondition,
           'brokerageBindMode': self.brokerageBindMode,
           'brokeragePosterUrls': self.brokeragePosterUrls,
           'brokerageFirstPercent': self.brokerageFirstPercent,
           'brokerageSecondPercent': self.brokerageSecondPercent,
           'brokerageWithdrawMinPrice': self.brokerageWithdrawMinPrice,
           'brokerageWithdrawFeePercent': self.brokerageWithdrawFeePercent,
           'brokerageFrozenDays': self.brokerageFrozenDays,
           'brokerageWithdrawTypes': self.brokerageWithdrawTypes,
           'creator': self.creator,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updater': self.updater,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'deleted': self.deleted,
           'tenantId': self.tenantId,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'afterSaleRefundReasons': self.afterSaleRefundReasons,
           'afterSaleReturnReasons': self.afterSaleReturnReasons,
           'deliveryExpressFreeEnabled': self.deliveryExpressFreeEnabled,
           'deliveryExpressFreePrice': self.deliveryExpressFreePrice,
           'deliveryPickUpEnabled': self.deliveryPickUpEnabled,
           'brokerageEnabled': self.brokerageEnabled,
           'brokerageEnabledCondition': self.brokerageEnabledCondition,
           'brokerageBindMode': self.brokerageBindMode,
           'brokeragePosterUrls': self.brokeragePosterUrls,
           'brokerageFirstPercent': self.brokerageFirstPercent,
           'brokerageSecondPercent': self.brokerageSecondPercent,
           'brokerageWithdrawMinPrice': self.brokerageWithdrawMinPrice,
           'brokerageWithdrawFeePercent': self.brokerageWithdrawFeePercent,
           'brokerageFrozenDays': self.brokerageFrozenDays,
           'brokerageWithdrawTypes': self.brokerageWithdrawTypes,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeConfig.id,TradeConfig.afterSaleRefundReasons,TradeConfig.afterSaleReturnReasons,TradeConfig.deliveryExpressFreeEnabled,TradeConfig.deliveryExpressFreePrice,TradeConfig.deliveryPickUpEnabled,TradeConfig.brokerageEnabled,TradeConfig.brokerageEnabledCondition,TradeConfig.brokerageBindMode,TradeConfig.brokeragePosterUrls,TradeConfig.brokerageFirstPercent,TradeConfig.brokerageSecondPercent,TradeConfig.brokerageWithdrawMinPrice,TradeConfig.brokerageWithdrawFeePercent,TradeConfig.brokerageFrozenDays,TradeConfig.brokerageWithdrawTypes]