from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String

class MessageSendSetting(BaseEntity, Base):
    __tablename__ = 'message_send_setting'

    Id = Column(String(36), comment='编号',primary_key=True)
    UID = Column(String(36), comment='用户编号')
    SendType = Column(Integer, comment='发送类型(1-微信 2-邮件 3-短信)')
    SendContent = Column(String(255), comment='发送内容')
    SendTemplateCode = Column(String(255), comment='短信模板')
    SendTemplateParam = Column(String(255), comment='短信模板参数')
    SendTemplateSign = Column(String(255), comment='短信签名')
    NextSendTime = Column(DateTime, comment='下次发送时间')
    LastSendTime = Column(DateTime, comment='最后发送时间')
    EventName = Column(String(36), comment='事件名称(birthday,anniversary,wedding,marriage,death,other)')
    EventId = Column(String(36), comment='事件编号')
    EventDate = Column(DateTime, comment='时间')
    EventDateIsLunar = Column(Integer, comment='是否是农历时间')
    PreDay = Column(Integer, comment='提前天数')
    Repetetion = Column(Integer, comment='重复(0-不重复 1-每天 2-每周 3-每月 4-每年)')
    Remark = Column(String(255), comment='备注')
    Status = Column(Integer, comment='状态(1-创建 3-待发送 4-发送中 9-失败 10-禁用)')
    IsDelete = Column(Integer, comment='删除')
    CreateUser = Column(String(20), comment='创建用户')
    CreateDate = Column(DateTime, comment='创建时间')
    LastModifiedUser = Column(String(20), comment='最后修改用户')
    LastModifiedDate = Column(DateTime, comment='最后修改时间')

    InsertRequireFields = ['SendType','EventName','Repetetion','PreDay','EventId']
    InsertOtherFields= ['NextSendTime', 'Status', 'IsDelete']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
            'Id': self.Id,
           'UID': self.UID,
           'SendType': self.SendType,
           'SendContent': self.SendContent,
           'SendTemplateCode': self.SendTemplateCode,
           'SendTemplateParam': self.SendTemplateParam,
           'SendTemplateSign': self.SendTemplateSign,
           'NextSendTime': self.NextSendTime,
           'Repetetion': self.Repetetion,
           'EventName': self.EventName,
           'EventDate': self.EventDate,
           'EventId': self.EventId,
           'PreDay': self.PreDay,
           'Status': self.Status,
           'IsDelete': self.IsDelete,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
           'LastModifiedUser': self.LastModifiedUser,
           'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回基本信息"""
        resp_dict = {
            'Id': self.Id,
           'UID': self.UID,
           'SendType': self.SendType,
        #    'SendContent': self.SendContent,
        #    'SendTemplateCode': self.SendTemplateCode,
        #    'SendTemplateParam': self.SendTemplateParam,
        #    'SendTemplateSign': self.SendTemplateSign,
           'NextSendTime': self.NextSendTime.strftime("%Y-%m-%d") if self.NextSendTime else None,
           'Repetetion': self.Repetetion,
           'EventName': self.EventName,
           'EventDate': self.EventDate,
           'EventId': self.EventId,
           'PreDay': self.PreDay,
           'Status': self.Status,
        #    'IsDelete': self.IsDelete,
        #    'CreateUser': self.CreateUser,
        #    'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
        #    'LastModifiedUser': self.LastModifiedUser,
        #    'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,

        }
        return resp_dict