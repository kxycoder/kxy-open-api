from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayTransfer(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_transfer'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    no = Column('no',String(64), comment='转账单号')
    appId = Column('app_id',Integer, comment='应用编号')
    channelId = Column('channel_id',Integer, comment='转账渠道编号')
    channelCode = Column('channel_code',String(32), comment='转账渠道编码')
    merchantTransferId = Column('merchant_transfer_id',String(64), comment='商户转账单编号')
    type = Column('type',Integer, comment='类型')
    status = Column('status',Integer, comment='转账状态')
    successTime = Column('success_time',DateTime, comment='转账成功时间')
    price = Column('price',Integer, comment='转账金额，单位：分')
    subject = Column('subject',String(512), comment='转账标题')
    userName = Column('user_name',String(64), comment='收款人姓名')
    alipayLogonId = Column('alipay_logon_id',String(64), comment='支付宝登录号')
    openid = Column('openid',String(64), comment='微信 openId')
    notifyUrl = Column('notify_url',String(1024), comment='异步通知商户地址')
    userIp = Column('user_ip',String(50), comment='用户 IP')
    channelExtras = Column('channel_extras',String(512), comment='渠道的额外参数')
    channelTransferNo = Column('channel_transfer_no',String(64), comment='渠道转账单号')
    channelErrorCode = Column('channel_error_code',String(128), comment='调用渠道的错误码')
    channelErrorMsg = Column('channel_error_msg',String(256), comment='调用渠道的错误提示')
    channelNotifyData = Column('channel_notify_data',String(4096), comment='渠道的同步/异步通知的内容')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['appId', 'channelId', 'type', 'status', 'price']
    InsertOtherFields= ['no', 'channelCode', 'merchantTransferId', 'successTime', 'subject', 'userName', 'alipayLogonId', 'openid', 'notifyUrl', 'userIp', 'channelExtras', 'channelTransferNo', 'channelErrorCode', 'channelErrorMsg', 'channelNotifyData']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'no': self.no,
           'appId': self.appId,
           'channelId': self.channelId,
           'channelCode': self.channelCode,
           'merchantTransferId': self.merchantTransferId,
           'type': self.type,
           'status': self.status,
           'successTime': self.successTime.strftime("%Y-%m-%d %H:%M:%S") if self.successTime else None,
           'price': self.price,
           'subject': self.subject,
           'userName': self.userName,
           'alipayLogonId': self.alipayLogonId,
           'openid': self.openid,
           'notifyUrl': self.notifyUrl,
           'userIp': self.userIp,
           'channelExtras': self.channelExtras,
           'channelTransferNo': self.channelTransferNo,
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
           'merchantTransferId': self.merchantTransferId,
           'type': self.type,
           'successTime': self.successTime,
           'price': self.price,
           'subject': self.subject,
           'userName': self.userName,
           'alipayLogonId': self.alipayLogonId,
           'openid': self.openid,
           'notifyUrl': self.notifyUrl,
           'userIp': self.userIp,
           'channelExtras': self.channelExtras,
           'channelTransferNo': self.channelTransferNo,
           'channelErrorCode': self.channelErrorCode,
           'channelErrorMsg': self.channelErrorMsg,
           'channelNotifyData': self.channelNotifyData,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayTransfer.id,PayTransfer.no,PayTransfer.appId,PayTransfer.channelId,PayTransfer.channelCode,PayTransfer.merchantTransferId,PayTransfer.type,PayTransfer.successTime,PayTransfer.price,PayTransfer.subject,PayTransfer.userName,PayTransfer.alipayLogonId,PayTransfer.openid,PayTransfer.notifyUrl,PayTransfer.userIp,PayTransfer.channelExtras,PayTransfer.channelTransferNo,PayTransfer.channelErrorCode,PayTransfer.channelErrorMsg,PayTransfer.channelNotifyData]