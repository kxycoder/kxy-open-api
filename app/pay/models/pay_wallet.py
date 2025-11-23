from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayWallet(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_wallet'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='用户编号')
    userType = Column('user_type',Integer, comment='用户类型')
    balance = Column('balance',Integer, comment='余额，单位分')
    totalExpense = Column('total_expense',Integer, comment='累计支出，单位分')
    totalRecharge = Column('total_recharge',Integer, comment='累计充值，单位分')
    freezePrice = Column('freeze_price',Integer, comment='冻结金额，单位分')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['userId', 'userType', 'balance', 'totalExpense', 'totalRecharge', 'freezePrice']
    InsertOtherFields= []


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'userType': self.userType,
           'balance': self.balance,
           'totalExpense': self.totalExpense,
           'totalRecharge': self.totalRecharge,
           'freezePrice': self.freezePrice,
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
           'balance': self.balance,
           'totalExpense': self.totalExpense,
           'totalRecharge': self.totalRecharge,
           'freezePrice': self.freezePrice,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayWallet.id,PayWallet.userId,PayWallet.userType,PayWallet.balance,PayWallet.totalExpense,PayWallet.totalRecharge,PayWallet.freezePrice]