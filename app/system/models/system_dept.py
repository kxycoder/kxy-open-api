from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter import FilterTenant
from kxy.framework.base_entity import JSONString

@FilterTenant('tenantId')
class SystemDept(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_dept'

    id = Column('id',BigInteger, comment='部门id',primary_key=True,autoincrement=True)
    name = Column('name',String(30), comment='部门名称')
    parentId = Column('parent_id',BigInteger, comment='父部门id')
    sort = Column('sort',Integer, comment='显示顺序')
    leaderUserId = Column('leader_user_id',BigInteger, comment='负责人')
    defaultRoles = Column('default_roles',JSONString(255), comment='默认角色')
    phone = Column('phone',String(11), comment='联系电话')
    email = Column('email',String(50), comment='邮箱')
    status = Column('status',Integer, comment='部门状态（0正常 1停用）')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',BigInteger, comment='租户编号')


    InsertRequireFields = []

    InsertOtherFields= ['name', 'leaderUserId','defaultRoles', 'phone', 'email','parentId', 'sort', 'status', 'tenantId']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'parentId': self.parentId,
           'sort': self.sort,
           'leaderUserId': self.leaderUserId,
           'defaultRoles': self.defaultRoles,
           'phone': self.phone,
           'email': self.email,
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
           'parentId': self.parentId,
           'sort': self.sort,
           'leaderUserId': self.leaderUserId,
           'defaultRoles': self.defaultRoles,
           'phone': self.phone,
           'email': self.email,
           'tenantId': self.tenantId,
        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemDept.id,SystemDept.name,SystemDept.parentId,SystemDept.sort]