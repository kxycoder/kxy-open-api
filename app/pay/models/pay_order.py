from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayOrder(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_order'


    id = Column('id',Integer, comment='支付订单编号',primary_key=True,autoincrement=True)
    appId = Column('app_id',Integer, comment='应用编号')
    channelId = Column('channel_id',Integer, comment='渠道编号')
    channelCode = Column('channel_code',String(32), comment='渠道编码')
    merchantOrderId = Column('merchant_order_id',String(64), comment='商户订单编号')
    subject = Column('subject',String(32), comment='商品标题')
    body = Column('body',String(128), comment='商品描述')
    notifyUrl = Column('notify_url',String(1024), comment='异步通知地址')
    price = Column('price',Integer, comment='支付金额，单位：分')
    channelFeeRate = Column('channel_fee_rate',String(0), comment='渠道手续费，单位：百分比')
    channelFeePrice = Column('channel_fee_price',Integer, comment='渠道手续金额，单位：分')
    status = Column('status',Integer, comment='支付状态')
    userIp = Column('user_ip',String(50), comment='用户 IP')
    expireTime = Column('expire_time',DateTime, comment='订单失效时间')
    successTime = Column('success_time',DateTime, comment='订单支付成功时间')
    extensionId = Column('extension_id',Integer, comment='支付成功的订单拓展单编号')
    no = Column('no',String(64), comment='支付订单号')
    refundPrice = Column('refund_price',Integer, comment='退款总金额，单位：分')
    channelUserId = Column('channel_user_id',String(255), comment='渠道用户编号')
    channelOrderNo = Column('channel_order_no',String(64), comment='渠道订单号')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['appId', 'price', 'status', 'expireTime', 'refundPrice']
    InsertOtherFields= ['channelId', 'channelCode', 'merchantOrderId', 'subject', 'body', 'notifyUrl', 'channelFeeRate', 'channelFeePrice', 'userIp', 'successTime', 'extensionId', 'no', 'channelUserId', 'channelOrderNo']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'appId': self.appId,
           'channelId': self.channelId,
           'channelCode': self.channelCode,
           'merchantOrderId': self.merchantOrderId,
           'subject': self.subject,
           'body': self.body,
           'notifyUrl': self.notifyUrl,
           'price': self.price,
           'channelFeeRate': self.channelFeeRate,
           'channelFeePrice': self.channelFeePrice,
           'status': self.status,
           'userIp': self.userIp,
           'expireTime': self.expireTime.strftime("%Y-%m-%d %H:%M:%S") if self.expireTime else None,
           'successTime': self.successTime.strftime("%Y-%m-%d %H:%M:%S") if self.successTime else None,
           'extensionId': self.extensionId,
           'no': self.no,
           'refundPrice': self.refundPrice,
           'channelUserId': self.channelUserId,
           'channelOrderNo': self.channelOrderNo,
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
           'appId': self.appId,
           'channelId': self.channelId,
           'channelCode': self.channelCode,
           'merchantOrderId': self.merchantOrderId,
           'subject': self.subject,
           'body': self.body,
           'notifyUrl': self.notifyUrl,
           'price': self.price,
           'channelFeeRate': self.channelFeeRate,
           'channelFeePrice': self.channelFeePrice,
           'userIp': self.userIp,
           'expireTime': self.expireTime,
           'successTime': self.successTime,
           'extensionId': self.extensionId,
           'no': self.no,
           'refundPrice': self.refundPrice,
           'channelUserId': self.channelUserId,
           'channelOrderNo': self.channelOrderNo,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayOrder.id,PayOrder.appId,PayOrder.channelId,PayOrder.channelCode,PayOrder.merchantOrderId,PayOrder.subject,PayOrder.body,PayOrder.notifyUrl,PayOrder.price,PayOrder.channelFeeRate,PayOrder.channelFeePrice,PayOrder.userIp,PayOrder.expireTime,PayOrder.successTime,PayOrder.extensionId,PayOrder.no,PayOrder.refundPrice,PayOrder.channelUserId,PayOrder.channelOrderNo]