from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayNotifyTask(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_notify_task'


    id = Column('id',Integer, comment='任务编号',primary_key=True,autoincrement=True)
    appId = Column('app_id',Integer, comment='应用编号')
    type = Column('type',Integer, comment='通知类型')
    dataId = Column('data_id',Integer, comment='数据编号')
    merchantOrderId = Column('merchant_order_id',String(64), comment='商户订单编号（商户系统生成）')
    merchantRefundId = Column('merchant_refund_id',String(64), comment='商户退款编号（商户系统生成）')
    merchantTransferId = Column('merchant_transfer_id',String(64), comment='商户转账编号（商户系统生成）')
    status = Column('status',Integer, comment='通知状态')
    nextNotifyTime = Column('next_notify_time',DateTime, comment='下一次通知时间')
    lastExecuteTime = Column('last_execute_time',DateTime, comment='最后一次执行时间')
    notifyTimes = Column('notify_times',Integer, comment='当前通知次数')
    maxNotifyTimes = Column('max_notify_times',Integer, comment='最大可通知次数')
    notifyUrl = Column('notify_url',String(1024), comment='异步通知商户地址')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['appId', 'type', 'dataId', 'status', 'nextNotifyTime', 'lastExecuteTime', 'notifyTimes', 'maxNotifyTimes']
    InsertOtherFields= ['merchantOrderId', 'merchantRefundId', 'merchantTransferId', 'notifyUrl']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'appId': self.appId,
           'type': self.type,
           'dataId': self.dataId,
           'merchantOrderId': self.merchantOrderId,
           'merchantRefundId': self.merchantRefundId,
           'merchantTransferId': self.merchantTransferId,
           'status': self.status,
           'nextNotifyTime': self.nextNotifyTime.strftime("%Y-%m-%d %H:%M:%S") if self.nextNotifyTime else None,
           'lastExecuteTime': self.lastExecuteTime.strftime("%Y-%m-%d %H:%M:%S") if self.lastExecuteTime else None,
           'notifyTimes': self.notifyTimes,
           'maxNotifyTimes': self.maxNotifyTimes,
           'notifyUrl': self.notifyUrl,
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
           'dataId': self.dataId,
           'merchantOrderId': self.merchantOrderId,
           'merchantRefundId': self.merchantRefundId,
           'merchantTransferId': self.merchantTransferId,
           'nextNotifyTime': self.nextNotifyTime,
           'lastExecuteTime': self.lastExecuteTime,
           'notifyTimes': self.notifyTimes,
           'maxNotifyTimes': self.maxNotifyTimes,
           'notifyUrl': self.notifyUrl,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayNotifyTask.id,PayNotifyTask.appId,PayNotifyTask.type,PayNotifyTask.dataId,PayNotifyTask.merchantOrderId,PayNotifyTask.merchantRefundId,PayNotifyTask.merchantTransferId,PayNotifyTask.nextNotifyTime,PayNotifyTask.lastExecuteTime,PayNotifyTask.notifyTimes,PayNotifyTask.maxNotifyTimes,PayNotifyTask.notifyUrl]