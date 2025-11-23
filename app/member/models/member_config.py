from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class MemberConfig(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'member_config'


    id = Column('id',Integer, comment='自增主键',primary_key=True,autoincrement=True)
    pointTradeDeductEnable = Column('point_trade_deduct_enable',Integer, comment='是否开启积分抵扣')
    pointTradeDeductUnitPrice = Column('point_trade_deduct_unit_price',Integer, comment='积分抵扣(单位：分)')
    pointTradeDeductMaxPrice = Column('point_trade_deduct_max_price',Integer, comment='积分抵扣最大值')
    pointTradeGivePoint = Column('point_trade_give_point',Integer, comment='1 元赠送多少分')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['pointTradeDeductEnable', 'pointTradeDeductUnitPrice']
    InsertOtherFields= ['pointTradeDeductMaxPrice', 'pointTradeGivePoint']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'pointTradeDeductEnable': self.pointTradeDeductEnable,
           'pointTradeDeductUnitPrice': self.pointTradeDeductUnitPrice,
           'pointTradeDeductMaxPrice': self.pointTradeDeductMaxPrice,
           'pointTradeGivePoint': self.pointTradeGivePoint,
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
           'pointTradeDeductEnable': self.pointTradeDeductEnable,
           'pointTradeDeductUnitPrice': self.pointTradeDeductUnitPrice,
           'pointTradeDeductMaxPrice': self.pointTradeDeductMaxPrice,
           'pointTradeGivePoint': self.pointTradeGivePoint,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [MemberConfig.id,MemberConfig.pointTradeDeductEnable,MemberConfig.pointTradeDeductUnitPrice,MemberConfig.pointTradeDeductMaxPrice,MemberConfig.pointTradeGivePoint]