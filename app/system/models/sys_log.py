from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String

class SysLog(BaseEntity, Base):
    __tablename__ = 'sys_log'

    Id = Column(String(30), comment='编号',primary_key=True)
    TableName = Column(String(100), comment='操作页面')
    Action = Column(String(100), comment='操作')
    ActionDate = Column(DateTime, comment='操作时间')
    Data = Column(String(0), comment='操作数据')
    CreateUser = Column(String(20), comment='创建用户')
    CreateDate = Column(DateTime, comment='创建时间')


    InsertRequireFields = ['TableName', 'Action']

    InsertOtherFields= ['Data','ActionDate']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
            'Id': self.Id,
           'TableName': self.TableName,
           'Action': self.Action,
           'ActionDate': self.ActionDate.strftime("%Y-%m-%d %H:%M:%S") if self.ActionDate else None,
           'Data': self.Data,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,

        }
        return resp_dict