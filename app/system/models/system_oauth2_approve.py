from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class SystemOauth2Approve(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_oauth2_approve'

    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='用户编号')
    userType = Column('user_type',Integer, comment='用户类型')
    clientId = Column('client_id',String(255), comment='客户端编号')
    scope = Column('scope',String(255), comment='授权范围')
    approved = Column('approved',String(1), comment='是否接受')
    expiresTime = Column('expires_time',DateTime, comment='过期时间')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['userId', 'userType', 'approved', 'expiresTime', 'tenantId']

    InsertOtherFields= ['clientId', 'scope']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'userType': self.userType,
           'clientId': self.clientId,
           'scope': self.scope,
           'approved': self.approved,
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
           'clientId': self.clientId,
           'scope': self.scope,
           'approved': self.approved,
           'expiresTime': self.expiresTime,
           'tenantId': self.tenantId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemOauth2Approve.id,SystemOauth2Approve.userId,SystemOauth2Approve.userType,SystemOauth2Approve.clientId,SystemOauth2Approve.scope,SystemOauth2Approve.approved,SystemOauth2Approve.expiresTime,SystemOauth2Approve.tenantId]