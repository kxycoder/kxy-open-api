from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayWalletRechargePackage(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_wallet_recharge_package'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    name = Column('name',String(64), comment='套餐名')
    payPrice = Column('pay_price',Integer, comment='支付金额')
    bonusPrice = Column('bonus_price',Integer, comment='赠送金额')
    status = Column('status',Integer, comment='状态')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['payPrice', 'bonusPrice', 'status']
    InsertOtherFields= ['name']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'payPrice': self.payPrice,
           'bonusPrice': self.bonusPrice,
           'status': self.status,
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
           'name': self.name,
           'payPrice': self.payPrice,
           'bonusPrice': self.bonusPrice,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayWalletRechargePackage.id,PayWalletRechargePackage.name,PayWalletRechargePackage.payPrice,PayWalletRechargePackage.bonusPrice]