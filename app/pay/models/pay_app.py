from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayApp(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_app'


    id = Column('id',Integer, comment='应用编号',primary_key=True,autoincrement=True)
    appKey = Column('app_key',String(64), comment='应用标识')
    name = Column('name',String(64), comment='应用名')
    status = Column('status',Integer, comment='开启状态')
    remark = Column('remark',String(255), comment='备注')
    orderNotifyUrl = Column('order_notify_url',String(1024), comment='支付结果的回调地址')
    refundNotifyUrl = Column('refund_notify_url',String(1024), comment='退款结果的回调地址')
    transferNotifyUrl = Column('transfer_notify_url',String(1024), comment='转账结果的回调地址')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['status']
    InsertOtherFields= ['appKey', 'name', 'remark', 'orderNotifyUrl', 'refundNotifyUrl', 'transferNotifyUrl']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'appKey': self.appKey,
           'name': self.name,
           'status': self.status,
           'remark': self.remark,
           'orderNotifyUrl': self.orderNotifyUrl,
           'refundNotifyUrl': self.refundNotifyUrl,
           'transferNotifyUrl': self.transferNotifyUrl,
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
           'appKey': self.appKey,
           'name': self.name,
           'remark': self.remark,
           'orderNotifyUrl': self.orderNotifyUrl,
           'refundNotifyUrl': self.refundNotifyUrl,
           'transferNotifyUrl': self.transferNotifyUrl,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayApp.id,PayApp.appKey,PayApp.name,PayApp.remark,PayApp.orderNotifyUrl,PayApp.refundNotifyUrl,PayApp.transferNotifyUrl]