from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String,BigInteger
from kxy.framework.filter import FilterTenant
@FilterTenant('tenantId')
class SystemOauth2RefreshToken(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int')
    __tablename__ = 'system_oauth2_refresh_token'

    id = Column('id',BigInteger, comment='编号',primary_key=True)
    userId = Column('user_id',BigInteger, comment='用户编号')
    refreshToken = Column('refresh_token',String(32), comment='刷新令牌')
    userType = Column('user_type',Integer, comment='用户类型')
    clientId = Column('client_id',String(255), comment='客户端编号')
    scopes = Column('scopes',String(255), comment='授权范围')
    expiresTime = Column('expires_time',DateTime, comment='过期时间')
    creator = Column('creator',BigInteger, comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',BigInteger, comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',BigInteger, comment='租户编号')


    InsertRequireFields = ['userId', 'userType', 'expiresTime']

    InsertOtherFields= ['refreshToken', 'clientId', 'scopes','tenantId']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'refreshToken': self.refreshToken,
           'userType': self.userType,
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
           'refreshToken': self.refreshToken,
           'userType': self.userType,
           'clientId': self.clientId,
           'scopes': self.scopes,
           'expiresTime': self.expiresTime,
           'tenantId': self.tenantId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemOauth2RefreshToken.id,SystemOauth2RefreshToken.userId,SystemOauth2RefreshToken.refreshToken,SystemOauth2RefreshToken.userType,SystemOauth2RefreshToken.clientId,SystemOauth2RefreshToken.scopes,SystemOauth2RefreshToken.expiresTime,SystemOauth2RefreshToken.tenantId]