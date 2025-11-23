from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String

class ExcelSettingDetail(BaseEntity, Base):
    __tablename__ = 'sys_excel_setting_detail'

    Id = Column(String(36), comment='编号',primary_key=True)
    BrandId = Column(String(36), comment='品牌编号')
    SettingId = Column(String(100), comment='配置编号')
    ExcelFieldName = Column(String(100), comment='excel列名')
    FieldName = Column(String(100), comment='字段名')
    FieldType = Column(String(100), comment='字段类型')
    Status = Column(Integer, comment='状态(1-创建 10-删除)')
    IsDelete = Column(Integer, comment='删除')
    CreateUser = Column(String(20), comment='创建用户')
    CreateDate = Column(DateTime, comment='创建时间')
    LastModifiedUser = Column(String(20), comment='最后修改用户')
    LastModifiedDate = Column(DateTime, comment='最后修改时间')
    CanExport = Column(Integer, comment='是否可导出')
    CanImport = Column(Integer, comment='是否可导入')



    InsertRequireFields = ['SettingId', 'ExcelFieldName', 'FieldName', 'FieldType']

    InsertOtherFields= ['BrandId', 'Status', 'IsDelete','CanExport','CanImport']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
                       'Id': self.Id,
           'BrandId': self.BrandId,
           'SettingId': self.SettingId,
           'ExcelFieldName': self.ExcelFieldName,
           'FieldName': self.FieldName,
           'FieldType': self.FieldType,
           'Status': self.Status,
           'IsDelete': self.IsDelete,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
           'LastModifiedUser': self.LastModifiedUser,
           'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,

        }
        return resp_dict