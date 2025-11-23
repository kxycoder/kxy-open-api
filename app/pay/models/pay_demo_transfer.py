from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayDemoTransfer(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_demo_transfer'


    id = Column('id',Integer, comment='订单编号',primary_key=True,autoincrement=True)
    appId = Column('app_id',Integer, comment='应用编号')
    type = Column('type',Integer, comment='转账类型')
    price = Column('price',Integer, comment='转账金额，单位：分')
    userName = Column('user_name',String(64), comment='收款人姓名')
    alipayLogonId = Column('alipay_logon_id',String(64), comment='支付宝登录号')
    openid = Column('openid',String(64), comment='微信 openId')
    transferStatus = Column('transfer_status',Integer, comment='转账状态')
    payTransferId = Column('pay_transfer_id',Integer, comment='转账订单编号')
    payChannelCode = Column('pay_channel_code',String(16), comment='转账支付成功渠道')
    transferTime = Column('transfer_time',DateTime, comment='转账支付时间')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['appId', 'type', 'price', 'transferStatus']
    InsertOtherFields= ['userName', 'alipayLogonId', 'openid', 'payTransferId', 'payChannelCode', 'transferTime']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'appId': self.appId,
           'type': self.type,
           'price': self.price,
           'userName': self.userName,
           'alipayLogonId': self.alipayLogonId,
           'openid': self.openid,
           'transferStatus': self.transferStatus,
           'payTransferId': self.payTransferId,
           'payChannelCode': self.payChannelCode,
           'transferTime': self.transferTime.strftime("%Y-%m-%d %H:%M:%S") if self.transferTime else None,
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
           'type': self.type,
           'price': self.price,
           'userName': self.userName,
           'alipayLogonId': self.alipayLogonId,
           'openid': self.openid,
           'transferStatus': self.transferStatus,
           'payTransferId': self.payTransferId,
           'payChannelCode': self.payChannelCode,
           'transferTime': self.transferTime,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayDemoTransfer.id,PayDemoTransfer.appId,PayDemoTransfer.type,PayDemoTransfer.price,PayDemoTransfer.userName,PayDemoTransfer.alipayLogonId,PayDemoTransfer.openid,PayDemoTransfer.transferStatus,PayDemoTransfer.payTransferId,PayDemoTransfer.payChannelCode,PayDemoTransfer.transferTime]