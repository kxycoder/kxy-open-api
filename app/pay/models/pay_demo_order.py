from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayDemoOrder(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_demo_order'


    id = Column('id',Integer, comment='订单编号',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='用户编号')
    spuId = Column('spu_id',Integer, comment='商品编号')
    spuName = Column('spu_name',String(255), comment='商品名字')
    price = Column('price',Integer, comment='价格，单位：分')
    payStatus = Column('pay_status',Integer, comment='是否已支付：[0:未支付 1:已经支付过]')
    payOrderId = Column('pay_order_id',Integer, comment='支付订单编号')
    payChannelCode = Column('pay_channel_code',String(16), comment='支付成功的支付渠道')
    payTime = Column('pay_time',DateTime, comment='订单支付时间')
    payRefundId = Column('pay_refund_id',Integer, comment='退款订单编号')
    refundPrice = Column('refund_price',Integer, comment='退款金额，单位：分')
    refundTime = Column('refund_time',DateTime, comment='退款时间')
    transferChannelPackageInfo = Column('transfer_channel_package_info',String(2048), comment='渠道 package 信息')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['spuId', 'price', 'payStatus', 'refundPrice']
    InsertOtherFields= ['userId', 'spuName', 'payOrderId', 'payChannelCode', 'payTime', 'payRefundId', 'refundTime', 'transferChannelPackageInfo']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'spuId': self.spuId,
           'spuName': self.spuName,
           'price': self.price,
           'payStatus': self.payStatus,
           'payOrderId': self.payOrderId,
           'payChannelCode': self.payChannelCode,
           'payTime': self.payTime.strftime("%Y-%m-%d %H:%M:%S") if self.payTime else None,
           'payRefundId': self.payRefundId,
           'refundPrice': self.refundPrice,
           'refundTime': self.refundTime.strftime("%Y-%m-%d %H:%M:%S") if self.refundTime else None,
           'transferChannelPackageInfo': self.transferChannelPackageInfo,
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
           'userId': self.userId,
           'spuId': self.spuId,
           'spuName': self.spuName,
           'price': self.price,
           'payStatus': self.payStatus,
           'payOrderId': self.payOrderId,
           'payChannelCode': self.payChannelCode,
           'payTime': self.payTime,
           'payRefundId': self.payRefundId,
           'refundPrice': self.refundPrice,
           'refundTime': self.refundTime,
           'transferChannelPackageInfo': self.transferChannelPackageInfo,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayDemoOrder.id,PayDemoOrder.userId,PayDemoOrder.spuId,PayDemoOrder.spuName,PayDemoOrder.price,PayDemoOrder.payStatus,PayDemoOrder.payOrderId,PayDemoOrder.payChannelCode,PayDemoOrder.payTime,PayDemoOrder.payRefundId,PayDemoOrder.refundPrice,PayDemoOrder.refundTime,PayDemoOrder.transferChannelPackageInfo]