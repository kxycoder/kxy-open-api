from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter import FilterTenant
from kxy.framework.base_entity import JSONString

@FilterTenant('tenantId')
class SystemRole(BaseEntity, Base):
    __tablename__ = 'system_role'
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)

    id = Column('id',Integer, comment='角色ID',primary_key=True,autoincrement=True)
    name = Column('name',String(30), comment='角色名称')
    code = Column('code',String(100), comment='角色权限字符串')
    sort = Column('sort',Integer, comment='显示顺序',default=0)
    dataScope = Column('data_scope',Integer, comment='数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）')
    dataScopeDeptIds = Column('data_scope_dept_ids',JSONString(500), comment='数据范围(指定部门数组)')
    status = Column('status',Integer, comment='角色状态（0正常 1停用）')
    type = Column('type',Integer, comment='角色类型',default=2)
    remark = Column('remark',String(500), comment='备注')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除')
    tenantId = Column('tenant_id',BigInteger, comment='租户编号')


    InsertRequireFields = []

    InsertOtherFields= ['name', 'code', 'dataScopeDeptIds', 'remark','sort', 'dataScope', 'status', 'type']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'code': self.code,
           'sort': self.sort,
           'dataScope': self.dataScope,
           'dataScopeDeptIds': self.dataScopeDeptIds,
           'status': self.status,
           'type': self.type,
           'remark': self.remark,
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
           'code': self.code,
           'sort': self.sort,
           'dataScope': self.dataScope,
           'dataScopeDeptIds': self.dataScopeDeptIds,
           'type': self.type,
           'remark': self.remark,
           'tenantId': self.tenantId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemRole.id,SystemRole.name,SystemRole.code,SystemRole.sort,SystemRole.dataScope,SystemRole.dataScopeDeptIds,SystemRole.type,SystemRole.remark,SystemRole.tenantId]