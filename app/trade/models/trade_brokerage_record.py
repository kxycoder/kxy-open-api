from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class TradeBrokerageRecord(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'trade_brokerage_record'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='用户编号')
    bizId = Column('biz_id',String(64), comment='业务编号')
    bizType = Column('biz_type',Integer, comment='业务类型：1-订单，2-提现')
    title = Column('title',String(64), comment='标题')
    price = Column('price',Integer, comment='金额')
    totalPrice = Column('total_price',Integer, comment='当前总佣金')
    description = Column('description',String(500), comment='说明')
    status = Column('status',Integer, comment='状态：0-待结算，1-已结算，2-已取消')
    frozenDays = Column('frozen_days',Integer, comment='冻结时间（天）')
    unfreezeTime = Column('unfreeze_time',DateTime, comment='解冻时间')
    sourceUserLevel = Column('source_user_level',Integer, comment='来源用户等级')
    sourceUserId = Column('source_user_id',Integer, comment='来源用户编号')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')
    index = Column('INDEX',String(0), comment='用户编号')
    index = Column('INDEX',String(0), comment='业务')
    index = Column('INDEX',String(0), comment='INDEX')


    InsertRequireFields = ['userId', 'bizType', 'price', 'totalPrice', 'status', 'frozenDays', 'sourceUserLevel', 'sourceUserId']
    InsertOtherFields= ['bizId', 'title', 'description', 'unfreezeTime', 'index', 'index', 'index']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'bizId': self.bizId,
           'bizType': self.bizType,
           'title': self.title,
           'price': self.price,
           'totalPrice': self.totalPrice,
           'description': self.description,
           'status': self.status,
           'frozenDays': self.frozenDays,
           'unfreezeTime': self.unfreezeTime.strftime("%Y-%m-%d %H:%M:%S") if self.unfreezeTime else None,
           'sourceUserLevel': self.sourceUserLevel,
           'sourceUserId': self.sourceUserId,
           'creator': self.creator,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updater': self.updater,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'deleted': self.deleted,
           'tenantId': self.tenantId,
           'index': self.index,
           'index': self.index,
           'index': self.index,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'bizId': self.bizId,
           'bizType': self.bizType,
           'title': self.title,
           'price': self.price,
           'totalPrice': self.totalPrice,
           'description': self.description,
           'frozenDays': self.frozenDays,
           'unfreezeTime': self.unfreezeTime,
           'sourceUserLevel': self.sourceUserLevel,
           'sourceUserId': self.sourceUserId,
           'index': self.index,
           'index': self.index,
           'index': self.index,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeBrokerageRecord.id,TradeBrokerageRecord.userId,TradeBrokerageRecord.bizId,TradeBrokerageRecord.bizType,TradeBrokerageRecord.title,TradeBrokerageRecord.price,TradeBrokerageRecord.totalPrice,TradeBrokerageRecord.description,TradeBrokerageRecord.frozenDays,TradeBrokerageRecord.unfreezeTime,TradeBrokerageRecord.sourceUserLevel,TradeBrokerageRecord.sourceUserId,TradeBrokerageRecord.index,TradeBrokerageRecord.index,TradeBrokerageRecord.index]