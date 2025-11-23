from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String

class SysUserExtend(BaseEntity, Base):
    __tablename__ = 'sys_user_extend'

    Id = Column(String(36), comment='用户编号',primary_key=True)
    Count = Column(Integer, comment='可以设置提醒的数量')
    LastCountTime = Column(DateTime, comment='最后统计时间')
    UnReadMsg = Column(Integer, comment='未读消息数量')
    Status = Column(Integer, comment='状态(1-创建 5-分享中 10-禁用)')
    IsDelete = Column(Integer, comment='删除')
    CreateUser = Column(String(20), comment='创建用户')
    CreateDate = Column(DateTime, comment='创建时间')
    LastModifiedUser = Column(String(20), comment='最后修改用户')
    LastModifiedDate = Column(DateTime, comment='最后修改时间')


    InsertRequireFields = []

    InsertOtherFields= ['Count', 'LastCountTime', 'Status', 'IsDelete']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'Id': self.Id,
           'Count': self.Count,
           'LastCountTime': self.LastCountTime,
           'UnReadMsg': self.UnReadMsg,
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
           'Count': self.Count,
        #    'LastCountTime': self.LastCountTime,
           'UnReadMsg': self.UnReadMsg
        }
        return resp_dict