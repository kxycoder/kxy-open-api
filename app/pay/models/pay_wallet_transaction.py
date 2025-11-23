from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayWalletTransaction(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_wallet_transaction'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    walletId = Column('wallet_id',Integer, comment='会员钱包 id')
    bizType = Column('biz_type',Integer, comment='关联类型')
    bizId = Column('biz_id',String(64), comment='关联业务编号')
    no = Column('no',String(64), comment='流水号')
    title = Column('title',String(128), comment='流水标题')
    price = Column('price',Integer, comment='交易金额, 单位分')
    balance = Column('balance',Integer, comment='余额, 单位分')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['walletId', 'bizType', 'price', 'balance']
    InsertOtherFields= ['bizId', 'no', 'title']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'walletId': self.walletId,
           'bizType': self.bizType,
           'bizId': self.bizId,
           'no': self.no,
           'title': self.title,
           'price': self.price,
           'balance': self.balance,
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
           'walletId': self.walletId,
           'bizType': self.bizType,
           'bizId': self.bizId,
           'no': self.no,
           'title': self.title,
           'price': self.price,
           'balance': self.balance,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayWalletTransaction.id,PayWalletTransaction.walletId,PayWalletTransaction.bizType,PayWalletTransaction.bizId,PayWalletTransaction.no,PayWalletTransaction.title,PayWalletTransaction.price,PayWalletTransaction.balance]