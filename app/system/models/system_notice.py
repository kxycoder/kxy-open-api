from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String
from kxy.framework.filter import FilterTenant

@FilterTenant('tenantId')
class SystemNotice(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_notice'

    id = Column('id',Integer, comment='公告ID',primary_key=True,autoincrement=True)
    title = Column('title',String(50), comment='公告标题')
    content = Column('content',String(0), comment='公告内容')
    type = Column('type',Integer, comment='公告类型（1通知 2公告）')
    status = Column('status',Integer, comment='公告状态（0正常 1关闭）')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除')
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = []

    InsertOtherFields= ['title', 'content','type', 'status']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'title': self.title,
           'content': self.content,
           'type': self.type,
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
           'title': self.title,
           'content': self.content,
           'type': self.type,
           'tenantId': self.tenantId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemNotice.id,SystemNotice.title,SystemNotice.content,SystemNotice.type,SystemNotice.tenantId]