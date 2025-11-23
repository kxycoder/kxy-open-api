from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class TradeBrokerageUser(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'trade_brokerage_user'


    id = Column('id',Integer, comment='用户编号',primary_key=True,autoincrement=True)
    bindUserId = Column('bind_user_id',Integer, comment='推广员编号')
    bindUserTime = Column('bind_user_time',DateTime, comment='推广员绑定时间')
    brokerageEnabled = Column('brokerage_enabled',Integer, comment='是否成为推广员')
    brokerageTime = Column('brokerage_time',DateTime, comment='成为分销员时间')
    brokeragePrice = Column('brokerage_price',Integer, comment='可用佣金')
    frozenPrice = Column('frozen_price',Integer, comment='冻结佣金')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['brokerageEnabled', 'brokeragePrice', 'frozenPrice']
    InsertOtherFields= ['bindUserId', 'bindUserTime', 'brokerageTime']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'bindUserId': self.bindUserId,
           'bindUserTime': self.bindUserTime.strftime("%Y-%m-%d %H:%M:%S") if self.bindUserTime else None,
           'brokerageEnabled': self.brokerageEnabled,
           'brokerageTime': self.brokerageTime.strftime("%Y-%m-%d %H:%M:%S") if self.brokerageTime else None,
           'brokeragePrice': self.brokeragePrice,
           'frozenPrice': self.frozenPrice,
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
           'bindUserId': self.bindUserId,
           'bindUserTime': self.bindUserTime,
           'brokerageEnabled': self.brokerageEnabled,
           'brokerageTime': self.brokerageTime,
           'brokeragePrice': self.brokeragePrice,
           'frozenPrice': self.frozenPrice,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeBrokerageUser.id,TradeBrokerageUser.bindUserId,TradeBrokerageUser.bindUserTime,TradeBrokerageUser.brokerageEnabled,TradeBrokerageUser.brokerageTime,TradeBrokerageUser.brokeragePrice,TradeBrokerageUser.frozenPrice]