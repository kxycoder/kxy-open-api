from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter import FilterTenant

@FilterTenant('tenantId')
class SystemPost(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_post'

    id = Column('id',Integer, comment='岗位ID',primary_key=True,autoincrement=True)
    code = Column('code',String(64), comment='岗位编码')
    name = Column('name',String(50), comment='岗位名称')
    sort = Column('sort',Integer, comment='显示顺序')
    status = Column('status',Integer, comment='状态（0正常 1停用）')
    remark = Column('remark',String(500), comment='备注')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['sort',]

    InsertOtherFields= ['code', 'name', 'remark', 'status', 'tenantId']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'code': self.code,
           'name': self.name,
           'sort': self.sort,
           'status': self.status,
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
           'code': self.code,
           'name': self.name,
           'sort': self.sort,
           'remark': self.remark,
           'tenantId': self.tenantId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemPost.id,SystemPost.code,SystemPost.name,SystemPost.sort,SystemPost.remark,SystemPost.tenantId]