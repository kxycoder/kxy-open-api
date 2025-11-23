from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.base_entity import JSONString

class SystemSmsTemplate(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_sms_template'

    id = Column('id',BigInteger, comment='编号',primary_key=True,autoincrement=True)
    type = Column('type',Integer, comment='模板类型')
    status = Column('status',Integer, comment='开启状态')
    code = Column('code',String(63), comment='模板编码')
    name = Column('name',String(63), comment='模板名称')
    content = Column('content',String(255), comment='模板内容')
    params = Column('params',JSONString(255), comment='参数数组')
    remark = Column('remark',String(255), comment='备注')
    apiTemplateId = Column('api_template_id',String(63), comment='短信 API 的模板编号')
    channelId = Column('channel_id',BigInteger, comment='短信渠道编号')
    channelCode = Column('channel_code',String(63), comment='短信渠道编码')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = ['type', 'status', 'channelId']

    InsertOtherFields= ['code', 'name', 'content', 'params', 'remark', 'apiTemplateId', 'channelCode']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'type': self.type,
           'status': self.status,
           'code': self.code,
           'name': self.name,
           'content': self.content,
           'params': self.params,
           'remark': self.remark,
           'apiTemplateId': self.apiTemplateId,
           'channelId': self.channelId,
           'channelCode': self.channelCode,
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
           'type': self.type,
           'code': self.code,
           'name': self.name,
           'content': self.content,
           'params': self.params,
           'remark': self.remark,
           'apiTemplateId': self.apiTemplateId,
           'channelId': self.channelId,
           'channelCode': self.channelCode,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemSmsTemplate.id,SystemSmsTemplate.type,SystemSmsTemplate.code,SystemSmsTemplate.name,SystemSmsTemplate.content,SystemSmsTemplate.params,SystemSmsTemplate.remark,SystemSmsTemplate.apiTemplateId,SystemSmsTemplate.channelId,SystemSmsTemplate.channelCode]