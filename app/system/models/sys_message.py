from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String

class SysMessage(BaseEntity, Base):
    __tablename__ = 'sys_message'

    Id = Column(String(36), comment='Id',primary_key=True)
    UID = Column(String(36), comment='UID')
    IsRead = Column(Integer, comment='IsRead')
    MsgType = Column(Integer, comment='1: 公告; 2: 活动 3:提醒')
    Title = Column(String(255), comment='Title')
    Content = Column(String(0), comment='Content')
    Status = Column(Integer, comment='状态(1-创建 10-删除)')
    IsDelete = Column(Integer, comment='删除')
    CreateUser = Column(String(20), comment='创建用户')
    CreateDate = Column(DateTime, comment='创建时间')
    LastModifiedUser = Column(String(20), comment='最后修改用户')
    LastModifiedDate = Column(DateTime, comment='最后修改时间')


    InsertRequireFields = ['Title', 'Content']

    InsertOtherFields= ['UID', 'IsRead', 'MsgType', 'Status', 'IsDelete']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'Id': self.Id,
           'UID': self.UID,
           'IsRead': self.IsRead,
           'MsgType': self.MsgType,
           'Title': self.Title,
           'Content': self.Content,
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
           'IsRead': self.IsRead,
           'MsgType': self.MsgType,
           'Title': self.Title,
           'Content': self.Content,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None
        }
        return resp_dict
