from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class TradeDeliveryExpress(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'trade_delivery_express'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    code = Column('code',String(64), comment='快递公司编码')
    name = Column('name',String(64), comment='快递公司名称')
    logo = Column('logo',String(256), comment='快递公司 logo')
    sort = Column('sort',Integer, comment='排序')
    status = Column('status',Integer, comment='状态')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['sort', 'status']
    InsertOtherFields= ['code', 'name', 'logo']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'code': self.code,
           'name': self.name,
           'logo': self.logo,
           'sort': self.sort,
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
           'code': self.code,
           'name': self.name,
           'logo': self.logo,
           'sort': self.sort,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeDeliveryExpress.id,TradeDeliveryExpress.code,TradeDeliveryExpress.name,TradeDeliveryExpress.logo,TradeDeliveryExpress.sort]