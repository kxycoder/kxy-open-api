from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayWalletRecharge(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_wallet_recharge'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    walletId = Column('wallet_id',Integer, comment='会员钱包 id')
    totalPrice = Column('total_price',Integer, comment='用户实际到账余额，例如充 100 送 20，则该值是 120')
    payPrice = Column('pay_price',Integer, comment='实际支付金额')
    bonusPrice = Column('bonus_price',Integer, comment='钱包赠送金额')
    packageId = Column('package_id',Integer, comment='充值套餐编号')
    payStatus = Column('pay_status',Integer, comment='是否已支付：[0:未支付 1:已经支付过]')
    payOrderId = Column('pay_order_id',Integer, comment='支付订单编号')
    payChannelCode = Column('pay_channel_code',String(16), comment='支付成功的支付渠道')
    payTime = Column('pay_time',DateTime, comment='订单支付时间')
    payRefundId = Column('pay_refund_id',Integer, comment='支付退款单编号')
    refundTotalPrice = Column('refund_total_price',Integer, comment='退款金额，包含赠送金额')
    refundPayPrice = Column('refund_pay_price',Integer, comment='退款支付金额')
    refundBonusPrice = Column('refund_bonus_price',Integer, comment='退款钱包赠送金额')
    refundTime = Column('refund_time',DateTime, comment='退款时间')
    refundStatus = Column('refund_status',Integer, comment='退款状态')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['walletId', 'totalPrice', 'payPrice', 'bonusPrice', 'payStatus', 'refundTotalPrice', 'refundPayPrice', 'refundBonusPrice', 'refundStatus']
    InsertOtherFields= ['packageId', 'payOrderId', 'payChannelCode', 'payTime', 'payRefundId', 'refundTime']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'walletId': self.walletId,
           'totalPrice': self.totalPrice,
           'payPrice': self.payPrice,
           'bonusPrice': self.bonusPrice,
           'packageId': self.packageId,
           'payStatus': self.payStatus,
           'payOrderId': self.payOrderId,
           'payChannelCode': self.payChannelCode,
           'payTime': self.payTime.strftime("%Y-%m-%d %H:%M:%S") if self.payTime else None,
           'payRefundId': self.payRefundId,
           'refundTotalPrice': self.refundTotalPrice,
           'refundPayPrice': self.refundPayPrice,
           'refundBonusPrice': self.refundBonusPrice,
           'refundTime': self.refundTime.strftime("%Y-%m-%d %H:%M:%S") if self.refundTime else None,
           'refundStatus': self.refundStatus,
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
           'walletId': self.walletId,
           'totalPrice': self.totalPrice,
           'payPrice': self.payPrice,
           'bonusPrice': self.bonusPrice,
           'packageId': self.packageId,
           'payStatus': self.payStatus,
           'payOrderId': self.payOrderId,
           'payChannelCode': self.payChannelCode,
           'payTime': self.payTime,
           'payRefundId': self.payRefundId,
           'refundTotalPrice': self.refundTotalPrice,
           'refundPayPrice': self.refundPayPrice,
           'refundBonusPrice': self.refundBonusPrice,
           'refundTime': self.refundTime,
           'refundStatus': self.refundStatus,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayWalletRecharge.id,PayWalletRecharge.walletId,PayWalletRecharge.totalPrice,PayWalletRecharge.payPrice,PayWalletRecharge.bonusPrice,PayWalletRecharge.packageId,PayWalletRecharge.payStatus,PayWalletRecharge.payOrderId,PayWalletRecharge.payChannelCode,PayWalletRecharge.payTime,PayWalletRecharge.payRefundId,PayWalletRecharge.refundTotalPrice,PayWalletRecharge.refundPayPrice,PayWalletRecharge.refundBonusPrice,PayWalletRecharge.refundTime,PayWalletRecharge.refundStatus]