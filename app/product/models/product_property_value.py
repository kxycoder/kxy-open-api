from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class ProductPropertyValue(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'product_property_value'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    propertyId = Column('property_id',Integer, comment='属性项的编号')
    name = Column('name',String(128), comment='名称')
    status = Column('status',Integer, comment='状态')
    remark = Column('remark',String(128), comment='备注')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    creator = Column('creator',String(64), comment='创建人')
    updater = Column('updater',String(64), comment='更新人')
    tenantId = Column('tenant_id',Integer, comment='租户编号')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = []
    InsertOtherFields= ['propertyId', 'name', 'status', 'remark']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'propertyId': self.propertyId,
           'name': self.name,
           'status': self.status,
           'remark': self.remark,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'creator': self.creator,
           'updater': self.updater,
           'tenantId': self.tenantId,
           'deleted': self.deleted,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'propertyId': self.propertyId,
           'name': self.name,
           'remark': self.remark,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [ProductPropertyValue.id,ProductPropertyValue.propertyId,ProductPropertyValue.name,ProductPropertyValue.remark]