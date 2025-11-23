from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class SystemOauth2Code(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_oauth2_code'

    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='用户编号')
    userType = Column('user_type',Integer, comment='用户类型')
    code = Column('code',String(32), comment='授权码')
    clientId = Column('client_id',String(255), comment='客户端编号')
    scopes = Column('scopes',String(255), comment='授权范围')
    expiresTime = Column('expires_time',DateTime, comment='过期时间')
    redirectUri = Column('redirect_uri',String(255), comment='可重定向的 URI 地址')
    state = Column('state',String(255), comment='状态')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['userId', 'userType', 'expiresTime', 'tenantId']

    InsertOtherFields= ['code', 'clientId', 'scopes', 'redirectUri', 'state']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'userType': self.userType,
           'code': self.code,
           'clientId': self.clientId,
           'scopes': self.scopes,
           'expiresTime': self.expiresTime.strftime("%Y-%m-%d %H:%M:%S") if self.expiresTime else None,
           'redirectUri': self.redirectUri,
           'state': self.state,
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
           'code': self.code,
           'clientId': self.clientId,
           'scopes': self.scopes,
           'expiresTime': self.expiresTime,
           'redirectUri': self.redirectUri,
           'state': self.state,
           'tenantId': self.tenantId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemOauth2Code.id,SystemOauth2Code.userId,SystemOauth2Code.userType,SystemOauth2Code.code,SystemOauth2Code.clientId,SystemOauth2Code.scopes,SystemOauth2Code.expiresTime,SystemOauth2Code.redirectUri,SystemOauth2Code.state,SystemOauth2Code.tenantId]