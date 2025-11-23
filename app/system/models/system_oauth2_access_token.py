from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter import FilterTenant
@FilterTenant('tenantId')
class SystemOauth2AccessToken(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int')
    __tablename__ = 'system_oauth2_access_token'

    id = Column('id',BigInteger, comment='编号',primary_key=True)
    userId = Column('user_id',BigInteger, comment='用户编号')
    userType = Column('user_type',Integer, comment='用户类型')
    userInfo = Column('user_info',String(512), comment='用户信息')
    accessToken = Column('access_token',String(255), comment='访问令牌')
    refreshToken = Column('refresh_token',String(32), comment='刷新令牌')
    clientId = Column('client_id',String(255), comment='客户端编号')
    scopes = Column('scopes',String(255), comment='授权范围')
    expiresTime = Column('expires_time',DateTime, comment='过期时间')
    creator = Column('creator',BigInteger, comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',BigInteger, comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')

    InsertRequireFields = []

    InsertOtherFields= ['userInfo', 'accessToken', 'refreshToken', 'clientId', 'scopes','tenantId','userId', 'userType', 'expiresTime']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'userType': self.userType,
           'userInfo': self.userInfo,
           'accessToken': self.accessToken,
           'refreshToken': self.refreshToken,
           'clientId': self.clientId,
           'scopes': self.scopes,
           'expiresTime': self.expiresTime.strftime("%Y-%m-%d %H:%M:%S") if self.expiresTime else None,
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
           'userInfo': self.userInfo,
           'accessToken': self.accessToken,
           'refreshToken': self.refreshToken,
           'clientId': self.clientId,
           'scopes': self.scopes,
           'expiresTime': self.expiresTime,
           'tenantId': self.tenantId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemOauth2AccessToken.id,SystemOauth2AccessToken.userId,SystemOauth2AccessToken.userType,SystemOauth2AccessToken.userInfo,SystemOauth2AccessToken.accessToken,SystemOauth2AccessToken.refreshToken,SystemOauth2AccessToken.clientId,SystemOauth2AccessToken.scopes,SystemOauth2AccessToken.expiresTime,SystemOauth2AccessToken.tenantId]