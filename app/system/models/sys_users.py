from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String,BigInteger

class SysUsers(BaseEntity, Base):
    __tablename__ = 'sys_users'
    def __init__(self):
        super().__init__(id_type='int')

    Id = Column(BigInteger, comment='编号',primary_key=True)
    Username = Column(String(30), comment='用户名')
    ChineseName = Column(String(45), comment='中文名')
    NickName = Column(String(45), comment='昵称')
    Email = Column(String(50), comment='Email')
    Password = Column(String(50), comment='用户密码')
    PhoneNumber = Column(String(18), comment='PhoneNumber')
    IsActive = Column(Integer, comment='是否启用')
    IsDelete = Column(Integer, comment='是否删除')
    Remark = Column(String(500), comment='员工描述内容')
    LastLoginDate = Column(DateTime, comment='最后登录日期')
    Status = Column(Integer, comment='状态')
    CreateUser = Column(String(36), comment='CreateUser')
    CreateDate = Column(DateTime, comment='创建日期')
    LastModifiedUser = Column(String(36), comment='LastModifiedUser')
    LastModifiedDate = Column(DateTime, comment='LastModifiedDate')
    OpenId = Column(String(36), comment='wxOpenId')
    Sex = Column(Integer, comment='性别')
    Avater = Column(String(500), comment='头像')
    RegistFrom = Column(String(20), comment='注册来源', default='')
    SourceId = Column(String(36), comment='来源编号')
    SourceType = Column(String(36), comment='来源类型')
    TenantId = Column(String(100), comment='租户编号')
    Roles = []


    InsertRequireFields = []

    InsertOtherFields= ['BrandId', 'Username', 'ChineseName', 'Email', 'Password', 'PhoneNumber', 'IsActive', 'IsDelete', 'Remark', 'LastLoginDate', 'Status', 'OpenId','Sex','Avater','SourceId','SourceType']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'Id': self.Id,
           'Username': self.Username,
           'ChineseName': self.ChineseName,
           'NickName': self.NickName,
           'Sex':self.Sex,
           'Avater':self.Avater,
           'Email': self.Email,
           'Password': self.Password,
           'PhoneNumber': self.PhoneNumber,
           'IsActive': self.IsActive,
           'IsDelete': self.IsDelete,
           'Remark': self.Remark,
           'LastLoginDate': self.LastLoginDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastLoginDate else None,
           'Status': self.Status,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
           'LastModifiedUser': self.LastModifiedUser,
           'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,
           'OpenId': self.OpenId,
           'SourceId':self.SourceId,
           'SourceType':self.SourceType,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回基本信息"""
        resp_dict = {
           'Id': self.Id,
           'Username': self.Username,
           'ChineseName': self.ChineseName,
           'NickName': self.NickName,
           'Sex':self.Sex,
           'Avater':self.Avater,
           'Email': self.Email,
           'PhoneNumber': self.PhoneNumber,
           'Remark': self.Remark
        }
        return resp_dict
    @staticmethod
    def get_simple_fields():
        return [SysUsers.Id,SysUsers.Username,SysUsers.ChineseName,SysUsers.NickName,SysUsers.Sex,SysUsers.Avater,SysUsers.Email,SysUsers.PhoneNumber,SysUsers.Remark]