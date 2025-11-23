from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String
from kxy.framework.base_entity import JSONString

class SystemNotifyTemplate(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_notify_template'

    id = Column('id',Integer, comment='主键',primary_key=True,autoincrement=True)
    name = Column('name',String(63), comment='模板名称')
    code = Column('code',String(64), comment='模版编码')
    nickname = Column('nickname',String(255), comment='发送人名称')
    content = Column('content',String(1024), comment='模版内容')
    type = Column('type',Integer, comment='类型')
    params = Column('params',JSONString(255), comment='参数数组')
    status = Column('status',Integer, comment='状态')
    remark = Column('remark',String(255), comment='备注')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除')


    InsertRequireFields = []

    InsertOtherFields= ['name', 'code', 'nickname', 'content', 'params', 'remark','type', 'status']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'code': self.code,
           'nickname': self.nickname,
           'content': self.content,
           'type': self.type,
           'params': self.params,
           'status': self.status,
           'remark': self.remark,
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
           'name': self.name,
           'code': self.code,
           'nickname': self.nickname,
           'content': self.content,
           'type': self.type,
           'params': self.params,
           'remark': self.remark,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemNotifyTemplate.id,SystemNotifyTemplate.name,SystemNotifyTemplate.code,SystemNotifyTemplate.nickname,SystemNotifyTemplate.content,SystemNotifyTemplate.type,SystemNotifyTemplate.params,SystemNotifyTemplate.remark]