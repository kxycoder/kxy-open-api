from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String

class PublicDictionaryType(BaseEntity, Base):
    __tablename__ = 'sys_public_dictionary_type'
    __description__ = '公共字典类型'

    Id = Column(String(36), comment='Id',primary_key=True)
    SystemCode = Column(String(200), comment='SystemCode')
    DicType = Column(String(45), comment='DicType')
    Description = Column(String(255), comment='描述')
    Status = Column(Integer, comment='状态 (0-创建 1- 激活 10-删除)')
    IsDelete = Column(Integer, comment='是否删除 (0-未删除 10-已删除)')
    CreateUser = Column(String(36), comment='创建人')
    CreateDate = Column(DateTime, comment='创建日期')
    LastModifiedUser = Column(String(36), comment='最后修改人')
    LastModifiedDate = Column(DateTime, comment='最后修改时间')
    CanEdit = Column(Integer, comment='是否可编辑 (0-不可编辑 1-可编辑)')
    Settings=[]

    InsertRequireFields = []

    InsertOtherFields= ['SystemCode', 'DicType', 'Description', 'Status', 'CanEdit']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
            'Id': self.Id,
           'SystemCode': self.SystemCode,
           'DicType': self.DicType,
           'Description': self.Description,
           'CanEdit': self.CanEdit,
           'Status': self.Status,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
           'LastModifiedUser': self.LastModifiedUser,
           'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,

        }
        return resp_dict