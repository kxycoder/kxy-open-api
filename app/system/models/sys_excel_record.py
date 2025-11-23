from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String

class ExcelRecord(BaseEntity, Base):
    __tablename__ = 'sys_excel_record'

    Id = Column(String(36), comment='编号',primary_key=True)
    TableName = Column(String(255), comment='表名')
    PageName = Column(String(255), comment='页面名称')
    Action = Column(String(10), comment='动作(import/export)')
    ExcelFile = Column(String(100), comment='excel文件路径')
    Status = Column(Integer, comment='状态(1-创建 4-失败 5-进行中 10-成功)')
    Remark = Column(String(2000), comment='失败原因')
    IsDelete = Column(Integer, comment='删除')
    CreateUser = Column(String(36), comment='创建用户')
    CreateUserName = Column(String(100), comment='创建用户名称')
    CreateDate = Column(DateTime, comment='创建时间')
    LastModifiedUser = Column(String(36), comment='最后修改用户')
    LastModifiedDate = Column(DateTime, comment='最后修改时间')


    InsertRequireFields = ['Action', 'ExcelFile']

    InsertOtherFields= ['TableName', 'PageName', 'Status', 'Remark', 'IsDelete']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
            'Id': self.Id,
           'TableName': self.TableName,
           'PageName': self.PageName,
           'Action': self.Action,
           'ExcelFile': self.ExcelFile,
           'Status': self.Status,
           'Remark': self.Remark,
           'IsDelete': self.IsDelete,
           'CreateUser': self.CreateUser,
           'CreateUserName': self.CreateUserName,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
           'LastModifiedUser': self.LastModifiedUser,
           'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,

        }
        return resp_dict