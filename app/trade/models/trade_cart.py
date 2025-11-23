from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class TradeCart(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'trade_cart'


    id = Column('id',Integer, comment='编号，唯一自增。',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='用户编号')
    spuId = Column('spu_id',Integer, comment='商品 SPU 编号')
    skuId = Column('sku_id',Integer, comment='商品 SKU 编号')
    count = Column('count',Integer, comment='商品购买数量')
    selected = Column('selected',Integer, comment='是否选中')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['userId', 'spuId', 'skuId', 'count', 'selected']
    InsertOtherFields= []


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'spuId': self.spuId,
           'skuId': self.skuId,
           'count': self.count,
           'selected': self.selected,
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
           'spuId': self.spuId,
           'skuId': self.skuId,
           'count': self.count,
           'selected': self.selected,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeCart.id,TradeCart.userId,TradeCart.spuId,TradeCart.skuId,TradeCart.count,TradeCart.selected]