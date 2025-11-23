from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.base_entity import JSONString

class SystemSmsLog(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_sms_log'

    id = Column('id',BigInteger, comment='编号',primary_key=True,autoincrement=True)
    channelId = Column('channel_id',BigInteger, comment='短信渠道编号')
    channelCode = Column('channel_code',String(63), comment='短信渠道编码')
    templateId = Column('template_id',BigInteger, comment='模板编号')
    templateCode = Column('template_code',String(63), comment='模板编码')
    templateType = Column('template_type',Integer, comment='短信类型')
    templateContent = Column('template_content',String(255), comment='短信内容')
    templateParams = Column('template_params',JSONString(255), comment='短信参数')
    apiTemplateId = Column('api_template_id',String(63), comment='短信 API 的模板编号')
    mobile = Column('mobile',String(11), comment='手机号')
    userId = Column('user_id',BigInteger, comment='用户编号')
    userType = Column('user_type',Integer, comment='用户类型')
    sendStatus = Column('send_status',Integer, comment='发送状态')
    sendTime = Column('send_time',DateTime, comment='发送时间')
    apiSendCode = Column('api_send_code',String(63), comment='短信 API 发送结果的编码')
    apiSendMsg = Column('api_send_msg',String(255), comment='短信 API 发送失败的提示')
    apiRequestId = Column('api_request_id',String(255), comment='短信 API 发送返回的唯一请求 ID')
    apiSerialNo = Column('api_serial_no',String(255), comment='短信 API 发送返回的序号')
    receiveStatus = Column('receive_status',Integer, comment='接收状态')
    receiveTime = Column('receive_time',DateTime, comment='接收时间')
    apiReceiveCode = Column('api_receive_code',String(63), comment='API 接收结果的编码')
    apiReceiveMsg = Column('api_receive_msg',String(255), comment='API 接收结果的说明')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    templateSign = ''


    InsertRequireFields = ['channelId', 'templateId', 'templateType', 'sendStatus', 'receiveStatus']

    InsertOtherFields= ['channelCode', 'templateCode', 'templateContent', 'templateParams', 'apiTemplateId', 'mobile', 'userId', 'userType', 'sendTime', 'apiSendCode', 'apiSendMsg', 'apiRequestId', 'apiSerialNo', 'receiveTime', 'apiReceiveCode', 'apiReceiveMsg']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'channelId': self.channelId,
           'channelCode': self.channelCode,
           'templateId': self.templateId,
           'templateCode': self.templateCode,
           'templateType': self.templateType,
           'templateContent': self.templateContent,
           'templateParams': self.templateParams,
           'apiTemplateId': self.apiTemplateId,
           'mobile': self.mobile,
           'userId': self.userId,
           'userType': self.userType,
           'sendStatus': self.sendStatus,
           'sendTime': self.sendTime.strftime("%Y-%m-%d %H:%M:%S") if self.sendTime else None,
           'apiSendCode': self.apiSendCode,
           'apiSendMsg': self.apiSendMsg,
           'apiRequestId': self.apiRequestId,
           'apiSerialNo': self.apiSerialNo,
           'receiveStatus': self.receiveStatus,
           'receiveTime': self.receiveTime.strftime("%Y-%m-%d %H:%M:%S") if self.receiveTime else None,
           'apiReceiveCode': self.apiReceiveCode,
           'apiReceiveMsg': self.apiReceiveMsg,
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
           'channelId': self.channelId,
           'channelCode': self.channelCode,
           'templateId': self.templateId,
           'templateCode': self.templateCode,
           'templateType': self.templateType,
           'templateContent': self.templateContent,
           'templateParams': self.templateParams,
           'apiTemplateId': self.apiTemplateId,
           'mobile': self.mobile,
           'userId': self.userId,
           'userType': self.userType,
           'sendStatus': self.sendStatus,
           'sendTime': self.sendTime,
           'apiSendCode': self.apiSendCode,
           'apiSendMsg': self.apiSendMsg,
           'apiRequestId': self.apiRequestId,
           'apiSerialNo': self.apiSerialNo,
           'receiveStatus': self.receiveStatus,
           'receiveTime': self.receiveTime,
           'apiReceiveCode': self.apiReceiveCode,
           'apiReceiveMsg': self.apiReceiveMsg,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemSmsLog.id,SystemSmsLog.channelId,SystemSmsLog.channelCode,SystemSmsLog.templateId,SystemSmsLog.templateCode,SystemSmsLog.templateType,SystemSmsLog.templateContent,SystemSmsLog.templateParams,SystemSmsLog.apiTemplateId,SystemSmsLog.mobile,SystemSmsLog.userId,SystemSmsLog.userType,SystemSmsLog.sendStatus,SystemSmsLog.sendTime,SystemSmsLog.apiSendCode,SystemSmsLog.apiSendMsg,SystemSmsLog.apiRequestId,SystemSmsLog.apiSerialNo,SystemSmsLog.receiveStatus,SystemSmsLog.receiveTime,SystemSmsLog.apiReceiveCode,SystemSmsLog.apiReceiveMsg]