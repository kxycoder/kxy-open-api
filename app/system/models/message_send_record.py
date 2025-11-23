from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String

class MessageSendRecord(BaseEntity, Base):
    __tablename__ = 'message_send_record'

    Id = Column(String(36), comment='编号',primary_key=True)
    MsgSettingId = Column(String(36), comment='配置编号')
    RequestId = Column(String(36), comment='请求编号')
    Phone = Column(String(30), comment='手机号')
    SendType = Column(String(255), comment='发送类型(1-微信 2-邮件 3-短信)')
    SendContent = Column(String(255), comment='发送内容')
    SendTemplateCode = Column(String(255), comment='短信模板')
    SendTemplateParam = Column(String(255), comment='短信模板参数')
    SendTime = Column(DateTime, comment='发送时间')
    EventName = Column(String(36), comment='事件名称')
    Remark = Column(String(255), comment='备注')
    Status = Column(Integer, comment='状态(1-创建 5-失败 10-成功)')
    IsDelete = Column(Integer, comment='删除')
    CreateUser = Column(String(20), comment='创建用户')
    CreateDate = Column(DateTime, comment='创建时间')


    InsertRequireFields = ['MsgSettingId', 'RequestId', 'Phone', 'SendType']

    InsertOtherFields= ['SendContent', 'SendTemplateCode', 'SendTemplateParam', 'SendTime', 'EventName', 'Status', 'IsDelete','Remark']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
            'Id': self.Id,
           'MsgSettingId': self.MsgSettingId,
           'RequestId': self.RequestId,
           'Phone': self.Phone,
           'SendType': self.SendType,
           'SendContent': self.SendContent,
           'SendTemplateCode': self.SendTemplateCode,
           'SendTemplateParam': self.SendTemplateParam,
           'SendTime': self.SendTime,
           'EventName': self.EventName,
           'Remark': self.Remark,
           'Status': self.Status,
           'IsDelete': self.IsDelete,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,

        }
        return resp_dict