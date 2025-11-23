from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class SystemMailLog(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_mail_log'

    id = Column('id',BigInteger, comment='编号',primary_key=True,autoincrement=True)
    userId = Column('user_id',BigInteger, comment='用户编号')
    userType = Column('user_type',Integer, comment='用户类型')
    toMail = Column('to_mail',String(255), comment='接收邮箱地址')
    accountId = Column('account_id',BigInteger, comment='邮箱账号编号')
    fromMail = Column('from_mail',String(255), comment='发送邮箱地址')
    templateId = Column('template_id',BigInteger, comment='模板编号')
    templateCode = Column('template_code',String(63), comment='模板编码')
    templateNickname = Column('template_nickname',String(255), comment='模版发送人名称')
    templateTitle = Column('template_title',String(255), comment='邮件标题')
    templateContent = Column('template_content',String(10240), comment='邮件内容')
    templateParams = Column('template_params',String(255), comment='邮件参数')
    sendStatus = Column('send_status',Integer, comment='发送状态')
    sendTime = Column('send_time',DateTime, comment='发送时间')
    sendMessageId = Column('send_message_id',String(255), comment='发送返回的消息 ID')
    sendException = Column('send_exception',String(4096), comment='发送异常')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = []

    InsertOtherFields= ['userId', 'userType', 'toMail', 'fromMail', 'templateCode', 'templateNickname', 'templateTitle', 'templateContent', 'templateParams', 'sendTime', 'sendMessageId', 'sendException','accountId', 'templateId', 'sendStatus']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'userType': self.userType,
           'toMail': self.toMail,
           'accountId': self.accountId,
           'fromMail': self.fromMail,
           'templateId': self.templateId,
           'templateCode': self.templateCode,
           'templateNickname': self.templateNickname,
           'templateTitle': self.templateTitle,
           'templateContent': self.templateContent,
           'templateParams': self.templateParams,
           'sendStatus': self.sendStatus,
           'sendTime': self.sendTime.strftime("%Y-%m-%d %H:%M:%S") if self.sendTime else None,
           'sendMessageId': self.sendMessageId,
           'sendException': self.sendException,
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
           'userId': self.userId,
           'userType': self.userType,
           'toMail': self.toMail,
           'accountId': self.accountId,
           'fromMail': self.fromMail,
           'templateId': self.templateId,
           'templateCode': self.templateCode,
           'templateNickname': self.templateNickname,
           'templateTitle': self.templateTitle,
           'templateContent': self.templateContent,
           'templateParams': self.templateParams,
           'sendStatus': self.sendStatus,
           'sendTime': self.sendTime,
           'sendMessageId': self.sendMessageId,
           'sendException': self.sendException,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemMailLog.id,SystemMailLog.userId,SystemMailLog.userType,SystemMailLog.toMail,SystemMailLog.accountId,SystemMailLog.fromMail,SystemMailLog.templateId,SystemMailLog.templateCode,SystemMailLog.templateNickname,SystemMailLog.templateTitle,SystemMailLog.templateContent,SystemMailLog.templateParams,SystemMailLog.sendStatus,SystemMailLog.sendTime,SystemMailLog.sendMessageId,SystemMailLog.sendException]