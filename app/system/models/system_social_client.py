from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger, Boolean
from kxy.framework.filter import FilterTenant
from kxy.framework.base_entity import JSONString

@FilterTenant()
class SystemSocialClient(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_social_client'

    id = Column('id',BigInteger, comment='编号',primary_key=True,autoincrement=True)
    name = Column('name',String(255), comment='应用名')
    socialType = Column('social_type',Integer, comment='社交平台的类型')
    userType = Column('user_type',Integer, comment='用户类型')
    clientId = Column('client_id',String(255), comment='客户端编号')
    clientSecret = Column('client_secret',String(255), comment='客户端密钥')
    agentId = Column('agent_id',String(255), comment='代理编号')
    autoRegistor = Column('auto_registor',Boolean, comment='是否自动注册')
    defaultRoles = Column('default_roles',JSONString(255), comment='默认角色')
    status = Column('status',Integer, comment='状态')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')
    redirectUri = ''

    InsertRequireFields = []

    InsertOtherFields= ['name', 'clientId', 'clientSecret', 'agentId','socialType', 'userType', 'status','autoRegistor','defaultRoles']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'socialType': self.socialType,
           'userType': self.userType,
           'clientId': self.clientId,
           'clientSecret': self.clientSecret,
           'agentId': self.agentId,
           'autoRegistor': self.autoRegistor,
           'defaultRoles': self.defaultRoles,
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
           'socialType': self.socialType,
           'userType': self.userType,
           'clientId': self.clientId,
           'clientSecret': self.clientSecret,
           'agentId': self.agentId,
           'tenantId': self.tenantId,
           'autoRegistor': self.autoRegistor,
           'defaultRoles': self.defaultRoles,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemSocialClient.id,SystemSocialClient.name,SystemSocialClient.socialType,SystemSocialClient.userType,SystemSocialClient.clientId,SystemSocialClient.clientSecret,SystemSocialClient.agentId,SystemSocialClient.tenantId,SystemSocialClient.autoRegistor,SystemSocialClient.defaultRoles]