from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.base_entity import JSONString

class SystemTenantPackage(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_tenant_package'

    id = Column('id',BigInteger, comment='套餐编号',primary_key=True,autoincrement=True)
    name = Column('name',String(30), comment='套餐名')
    status = Column('status',Integer, comment='租户状态（0正常 1停用）')
    remark = Column('remark',String(256), comment='备注')
    menuIds = Column('menu_ids',JSONString(4096), comment='关联的菜单编号')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除')


    InsertRequireFields = []

    InsertOtherFields= ['name', 'remark', 'menuIds','status']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'status': self.status,
           'remark': self.remark,
           'menuIds': self.menuIds,
           'creator': self.creator,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updater': self.updater,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'deleted': self.deleted,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'remark': self.remark,
           'menuIds': self.menuIds,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemTenantPackage.id,SystemTenantPackage.name,SystemTenantPackage.remark,SystemTenantPackage.menuIds]