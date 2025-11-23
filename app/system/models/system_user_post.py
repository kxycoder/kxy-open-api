from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter import FilterTenant

@FilterTenant('tenantId')
class SystemUserPost(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int')
    __tablename__ = 'system_user_post'

    id = Column('id',BigInteger, comment='id',primary_key=True)
    userId = Column('user_id',BigInteger, comment='用户ID')
    postId = Column('post_id',BigInteger, comment='岗位ID')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除')
    tenantId = Column('tenant_id',BigInteger, comment='租户编号')


    InsertRequireFields = []

    InsertOtherFields= ['userId', 'postId', 'tenantId']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'postId': self.postId,
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
           'postId': self.postId,
           'tenantId': self.tenantId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemUserPost.id,SystemUserPost.userId,SystemUserPost.postId,SystemUserPost.tenantId]