from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.base_entity import JSONString

class SystemMailTemplate(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_mail_template'

    id = Column('id',BigInteger, comment='编号',primary_key=True,autoincrement=True)
    name = Column('name',String(63), comment='模板名称')
    code = Column('code',String(63), comment='模板编码')
    accountId = Column('account_id',BigInteger, comment='发送的邮箱账号编号')
    nickname = Column('nickname',String(255), comment='发送人名称')
    title = Column('title',String(255), comment='模板标题')
    content = Column('content',String(10240), comment='模板内容')
    params = Column('params',JSONString(255), comment='参数数组')
    status = Column('status',Integer, comment='开启状态')
    remark = Column('remark',String(255), comment='备注')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = ['accountId', 'status']

    InsertOtherFields= ['name', 'code', 'nickname', 'title', 'content', 'params', 'remark']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'code': self.code,
           'accountId': self.accountId,
           'nickname': self.nickname,
           'title': self.title,
           'content': self.content,
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
           'accountId': self.accountId,
           'nickname': self.nickname,
           'title': self.title,
           'content': self.content,
           'params': self.params,
           'remark': self.remark,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemMailTemplate.id,SystemMailTemplate.name,SystemMailTemplate.code,SystemMailTemplate.accountId,SystemMailTemplate.nickname,SystemMailTemplate.title,SystemMailTemplate.content,SystemMailTemplate.params,SystemMailTemplate.remark]