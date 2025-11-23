from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class TradeOrderLog(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'trade_order_log'


    id = Column('id',Integer, comment='日志主键',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='用户编号')
    userType = Column('user_type',Integer, comment='用户类型')
    orderId = Column('order_id',Integer, comment='订单号')
    beforeStatus = Column('before_status',Integer, comment='操作前状态')
    afterStatus = Column('after_status',Integer, comment='操作后状态')
    operateType = Column('operate_type',Integer, comment='操作类型')
    content = Column('content',String(2000), comment='操作内容')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['userId', 'userType', 'orderId', 'operateType']
    InsertOtherFields= ['beforeStatus', 'afterStatus', 'content']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'userType': self.userType,
           'orderId': self.orderId,
           'beforeStatus': self.beforeStatus,
           'afterStatus': self.afterStatus,
           'operateType': self.operateType,
           'content': self.content,
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
           'userType': self.userType,
           'orderId': self.orderId,
           'beforeStatus': self.beforeStatus,
           'afterStatus': self.afterStatus,
           'operateType': self.operateType,
           'content': self.content,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeOrderLog.id,TradeOrderLog.userId,TradeOrderLog.userType,TradeOrderLog.orderId,TradeOrderLog.beforeStatus,TradeOrderLog.afterStatus,TradeOrderLog.operateType,TradeOrderLog.content]