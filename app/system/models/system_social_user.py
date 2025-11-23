from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.base_entity import JSONString
from kxy.framework.filter import FilterTenant

@FilterTenant()
class SystemSocialUser(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_social_user'

    id = Column('id',BigInteger, comment='主键(自增策略)',primary_key=True,autoincrement=True)
    type = Column('type',Integer, comment='社交平台的类型')
    openid = Column('openid',String(32), comment='社交 openid')
    token = Column('token',String(256), comment='社交 token')
    rawTokenInfo = Column('raw_token_info',JSONString(1024), comment='原始 Token 数据，一般是 JSON 格式')
    nickname = Column('nickname',String(32), comment='用户昵称')
    avatar = Column('avatar',String(255), comment='用户头像')
    rawUserInfo = Column('raw_user_info',JSONString(1024), comment='原始用户数据，一般是 JSON 格式')
    code = Column('code',String(256), comment='最后一次的认证 code')
    state = Column('state',String(256), comment='最后一次的认证 state')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = []

    InsertOtherFields= ['openid', 'token', 'rawTokenInfo', 'nickname', 'avatar', 'rawUserInfo', 'code', 'state','type']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'type': self.type,
           'openid': self.openid,
           'token': self.token,
           'rawTokenInfo': self.rawTokenInfo,
           'nickname': self.nickname,
           'avatar': self.avatar,
           'rawUserInfo': self.rawUserInfo,
           'code': self.code,
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
           'type': self.type,
           'openid': self.openid,
           'token': self.token,
           'rawTokenInfo': self.rawTokenInfo,
           'nickname': self.nickname,
           'avatar': self.avatar,
           'rawUserInfo': self.rawUserInfo,
           'code': self.code,
           'state': self.state,
           'tenantId': self.tenantId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemSocialUser.id,SystemSocialUser.type,SystemSocialUser.openid,SystemSocialUser.token,SystemSocialUser.rawTokenInfo,SystemSocialUser.nickname,SystemSocialUser.avatar,SystemSocialUser.rawUserInfo,SystemSocialUser.code,SystemSocialUser.state,SystemSocialUser.tenantId]