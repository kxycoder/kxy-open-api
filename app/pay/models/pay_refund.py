from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayRefund(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_refund'


    id = Column('id',Integer, comment='支付退款编号',primary_key=True,autoincrement=True)
    no = Column('no',String(64), comment='退款单号')
    appId = Column('app_id',Integer, comment='应用编号')
    channelId = Column('channel_id',Integer, comment='渠道编号')
    channelCode = Column('channel_code',String(32), comment='渠道编码')
    orderId = Column('order_id',Integer, comment='支付订单编号 pay_order 表id')
    orderNo = Column('order_no',String(64), comment='支付订单 no')
    merchantOrderId = Column('merchant_order_id',String(64), comment='商户订单编号（商户系统生成）')
    merchantRefundId = Column('merchant_refund_id',String(64), comment='商户退款订单号（商户系统生成）')
    notifyUrl = Column('notify_url',String(1024), comment='异步通知商户地址')
    status = Column('status',Integer, comment='退款状态')
    payPrice = Column('pay_price',Integer, comment='支付金额,单位分')
    refundPrice = Column('refund_price',Integer, comment='退款金额,单位分')
    reason = Column('reason',String(256), comment='退款原因')
    userIp = Column('user_ip',String(50), comment='用户 IP')
    channelOrderNo = Column('channel_order_no',String(64), comment='渠道订单号，pay_order 中的 channel_order_no 对应')
    channelRefundNo = Column('channel_refund_no',String(64), comment='渠道退款单号，渠道返回')
    successTime = Column('success_time',DateTime, comment='退款成功时间')
    channelErrorCode = Column('channel_error_code',String(128), comment='渠道调用报错时，错误码')
    channelErrorMsg = Column('channel_error_msg',String(256), comment='渠道调用报错时，错误信息')
    channelNotifyData = Column('channel_notify_data',String(4096), comment='支付渠道异步通知的内容')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['appId', 'channelId', 'orderId', 'status', 'payPrice', 'refundPrice']
    InsertOtherFields= ['no', 'channelCode', 'orderNo', 'merchantOrderId', 'merchantRefundId', 'notifyUrl', 'reason', 'userIp', 'channelOrderNo', 'channelRefundNo', 'successTime', 'channelErrorCode', 'channelErrorMsg', 'channelNotifyData']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'no': self.no,
           'appId': self.appId,
           'channelId': self.channelId,
           'channelCode': self.channelCode,
           'orderId': self.orderId,
           'orderNo': self.orderNo,
           'merchantOrderId': self.merchantOrderId,
           'merchantRefundId': self.merchantRefundId,
           'notifyUrl': self.notifyUrl,
           'status': self.status,
           'payPrice': self.payPrice,
           'refundPrice': self.refundPrice,
           'reason': self.reason,
           'userIp': self.userIp,
           'channelOrderNo': self.channelOrderNo,
           'channelRefundNo': self.channelRefundNo,
           'successTime': self.successTime.strftime("%Y-%m-%d %H:%M:%S") if self.successTime else None,
           'channelErrorCode': self.channelErrorCode,
           'channelErrorMsg': self.channelErrorMsg,
           'channelNotifyData': self.channelNotifyData,
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
           'no': self.no,
           'appId': self.appId,
           'channelId': self.channelId,
           'channelCode': self.channelCode,
           'orderId': self.orderId,
           'orderNo': self.orderNo,
           'merchantOrderId': self.merchantOrderId,
           'merchantRefundId': self.merchantRefundId,
           'notifyUrl': self.notifyUrl,
           'payPrice': self.payPrice,
           'refundPrice': self.refundPrice,
           'reason': self.reason,
           'userIp': self.userIp,
           'channelOrderNo': self.channelOrderNo,
           'channelRefundNo': self.channelRefundNo,
           'successTime': self.successTime,
           'channelErrorCode': self.channelErrorCode,
           'channelErrorMsg': self.channelErrorMsg,
           'channelNotifyData': self.channelNotifyData,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayRefund.id,PayRefund.no,PayRefund.appId,PayRefund.channelId,PayRefund.channelCode,PayRefund.orderId,PayRefund.orderNo,PayRefund.merchantOrderId,PayRefund.merchantRefundId,PayRefund.notifyUrl,PayRefund.payPrice,PayRefund.refundPrice,PayRefund.reason,PayRefund.userIp,PayRefund.channelOrderNo,PayRefund.channelRefundNo,PayRefund.successTime,PayRefund.channelErrorCode,PayRefund.channelErrorMsg,PayRefund.channelNotifyData]