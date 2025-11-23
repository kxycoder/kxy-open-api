from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayOrderExtension(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_order_extension'


    id = Column('id',Integer, comment='支付订单编号',primary_key=True,autoincrement=True)
    no = Column('no',String(64), comment='支付订单号')
    orderId = Column('order_id',Integer, comment='支付订单编号')
    channelId = Column('channel_id',Integer, comment='渠道编号')
    channelCode = Column('channel_code',String(32), comment='渠道编码')
    userIp = Column('user_ip',String(50), comment='用户 IP')
    status = Column('status',Integer, comment='支付状态')
    channelExtras = Column('channel_extras',String(256), comment='支付渠道的额外参数')
    channelErrorCode = Column('channel_error_code',String(128), comment='渠道调用报错时，错误码')
    channelErrorMsg = Column('channel_error_msg',String(256), comment='渠道调用报错时，错误信息')
    channelNotifyData = Column('channel_notify_data',String(4096), comment='支付渠道异步通知的内容')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['orderId', 'channelId', 'status']
    InsertOtherFields= ['no', 'channelCode', 'userIp', 'channelExtras', 'channelErrorCode', 'channelErrorMsg', 'channelNotifyData']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'no': self.no,
           'orderId': self.orderId,
           'channelId': self.channelId,
           'channelCode': self.channelCode,
           'userIp': self.userIp,
           'status': self.status,
           'channelExtras': self.channelExtras,
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
           'orderId': self.orderId,
           'channelId': self.channelId,
           'channelCode': self.channelCode,
           'userIp': self.userIp,
           'channelExtras': self.channelExtras,
           'channelErrorCode': self.channelErrorCode,
           'channelErrorMsg': self.channelErrorMsg,
           'channelNotifyData': self.channelNotifyData,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayOrderExtension.id,PayOrderExtension.no,PayOrderExtension.orderId,PayOrderExtension.channelId,PayOrderExtension.channelCode,PayOrderExtension.userIp,PayOrderExtension.channelExtras,PayOrderExtension.channelErrorCode,PayOrderExtension.channelErrorMsg,PayOrderExtension.channelNotifyData]