from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String
from kxy.framework.filter import FilterTenant
from kxy.framework.filter_user import FilterUser
from kxy.framework.base_entity import JSONString
@FilterUser('userId')
@FilterTenant('tenantId')
class SystemNotifyMessage(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_notify_message'

    id = Column('id',Integer, comment='用户ID',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='用户id')
    userType = Column('user_type',Integer, comment='用户类型')
    templateId = Column('template_id',Integer, comment='模版编号')
    templateCode = Column('template_code',String(64), comment='模板编码')
    templateNickname = Column('template_nickname',String(63), comment='模版发送人名称')
    templateContent = Column('template_content',String(1024), comment='模版内容')
    templateType = Column('template_type',Integer, comment='模版类型')
    templateParams = Column('template_params',JSONString(255), comment='模版参数')
    readStatus = Column('read_status',String(1), comment='是否已读',default=0)
    readTime = Column('read_time',DateTime, comment='阅读时间')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = []

    InsertOtherFields= ['templateCode', 'templateNickname', 'templateContent', 'templateParams', 'readTime', 'userId', 'userType', 'templateId', 'templateType', 'readStatus']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'userType': self.userType,
           'templateId': self.templateId,
           'templateCode': self.templateCode,
           'templateNickname': self.templateNickname,
           'templateContent': self.templateContent,
           'templateType': self.templateType,
           'templateParams': self.templateParams,
           'readStatus': self.readStatus,
           'readTime': self.readTime.strftime("%Y-%m-%d %H:%M:%S") if self.readTime else None,
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
           'templateId': self.templateId,
           'templateCode': self.templateCode,
           'templateNickname': self.templateNickname,
           'templateContent': self.templateContent,
           'templateType': self.templateType,
           'templateParams': self.templateParams,
           'readStatus': self.readStatus,
           'readTime': self.readTime,
           'tenantId': self.tenantId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemNotifyMessage.id,SystemNotifyMessage.userId,SystemNotifyMessage.userType,SystemNotifyMessage.templateId,SystemNotifyMessage.templateCode,SystemNotifyMessage.templateNickname,SystemNotifyMessage.templateContent,SystemNotifyMessage.templateType,SystemNotifyMessage.templateParams,SystemNotifyMessage.readStatus,SystemNotifyMessage.readTime,SystemNotifyMessage.tenantId]