from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class SystemOauth2Client(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_oauth2_client'

    id = Column('id',BigInteger, comment='编号',primary_key=True,autoincrement=True)
    clientId = Column('client_id',String(255), comment='客户端编号')
    secret = Column('secret',String(255), comment='客户端密钥')
    name = Column('name',String(255), comment='应用名')
    logo = Column('logo',String(255), comment='应用图标')
    description = Column('description',String(255), comment='应用描述')
    status = Column('status',Integer, comment='状态')
    accessTokenValiditySeconds = Column('access_token_validity_seconds',Integer, comment='访问令牌的有效期')
    refreshTokenValiditySeconds = Column('refresh_token_validity_seconds',Integer, comment='刷新令牌的有效期')
    redirectUris = Column('redirect_uris',String(255), comment='可重定向的 URI 地址')
    authorizedGrantTypes = Column('authorized_grant_types',String(255), comment='授权类型')
    scopes = Column('scopes',String(255), comment='授权范围')
    autoApproveScopes = Column('auto_approve_scopes',String(255), comment='自动通过的授权范围')
    authorities = Column('authorities',String(255), comment='权限')
    resourceIds = Column('resource_ids',String(255), comment='资源')
    additionalInformation = Column('additional_information',String(4096), comment='附加信息')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = ['status', 'accessTokenValiditySeconds', 'refreshTokenValiditySeconds']

    InsertOtherFields= ['clientId', 'secret', 'name', 'logo', 'description', 'redirectUris', 'authorizedGrantTypes', 'scopes', 'autoApproveScopes', 'authorities', 'resourceIds', 'additionalInformation']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'clientId': self.clientId,
           'secret': self.secret,
           'name': self.name,
           'logo': self.logo,
           'description': self.description,
           'status': self.status,
           'accessTokenValiditySeconds': self.accessTokenValiditySeconds,
           'refreshTokenValiditySeconds': self.refreshTokenValiditySeconds,
           'redirectUris': self.redirectUris,
           'authorizedGrantTypes': self.authorizedGrantTypes,
           'scopes': self.scopes,
           'autoApproveScopes': self.autoApproveScopes,
           'authorities': self.authorities,
           'resourceIds': self.resourceIds,
           'additionalInformation': self.additionalInformation,
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
           'clientId': self.clientId,
           'secret': self.secret,
           'name': self.name,
           'logo': self.logo,
           'description': self.description,
           'accessTokenValiditySeconds': self.accessTokenValiditySeconds,
           'refreshTokenValiditySeconds': self.refreshTokenValiditySeconds,
           'redirectUris': self.redirectUris,
           'authorizedGrantTypes': self.authorizedGrantTypes,
           'scopes': self.scopes,
           'autoApproveScopes': self.autoApproveScopes,
           'authorities': self.authorities,
           'resourceIds': self.resourceIds,
           'additionalInformation': self.additionalInformation,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemOauth2Client.id,SystemOauth2Client.clientId,SystemOauth2Client.secret,SystemOauth2Client.name,SystemOauth2Client.logo,SystemOauth2Client.description,SystemOauth2Client.accessTokenValiditySeconds,SystemOauth2Client.refreshTokenValiditySeconds,SystemOauth2Client.redirectUris,SystemOauth2Client.authorizedGrantTypes,SystemOauth2Client.scopes,SystemOauth2Client.autoApproveScopes,SystemOauth2Client.authorities,SystemOauth2Client.resourceIds,SystemOauth2Client.additionalInformation]