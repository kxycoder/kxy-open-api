from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class InfraTableFields(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'infra_table_fields'

    id = Column('id',Integer, comment='Id',primary_key=True,autoincrement=True)
    tableId = Column('table_id',Integer, comment='表Id')
    fieldName = Column('field_name',String(255), comment='字段名')
    isPrimaryKey = Column('is_primary_key',Integer, comment='是否主键')
    isAutoIncrement = Column('is_auto_increment',Integer, comment='自增')
    canNull = Column('can_null',Integer, comment='可空')
    dataType = Column('data_type',String(255), comment='类型')
    description = Column('description',String(255), comment='描述')
    length = Column('length',Integer, comment='长度')
    showInTable = Column('show_in_table',Integer, comment='在表格展示')
    showInForm = Column('show_in_form',Integer, comment='编辑展示')
    showDetail = Column('show_detail',Integer, comment='详情展示')
    showInSerch = Column('show_in_serch',Integer, comment='搜索条件')
    htmlType = Column('html_type',String(255), comment='html类型',default='input')
    dictType = Column('dict_type',String(255), comment='字典类型',default='')
    example = Column('example',String(255), comment='示例',default='')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = []

    InsertOtherFields= ['tableId', 'fieldName', 'isPrimaryKey', 'isAutoIncrement', 'canNull', 'dataType', 'description', 'length', 'showInTable', 'showInForm', 'showDetail', 'showInSerch','htmlType','dictType','example']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'tableId': self.tableId,
           'fieldName': self.fieldName,
           'isPrimaryKey': self.isPrimaryKey,
           'isAutoIncrement': self.isAutoIncrement,
           'canNull': self.canNull,
           'dataType': self.dataType,
           'description': self.description,
           'length': self.length,
           'showInTable': self.showInTable,
           'showInForm': self.showInForm,
           'showDetail': self.showDetail,
           'showInSerch': self.showInSerch,
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
           'tableId': self.tableId,
           'fieldName': self.fieldName,
           'isPrimaryKey': self.isPrimaryKey,
           'isAutoIncrement': self.isAutoIncrement,
           'canNull': self.canNull,
           'dataType': self.dataType,
           'description': self.description,
           'length': self.length,
           'showInTable': self.showInTable,
           'showInForm': self.showInForm,
           'showDetail': self.showDetail,
           'showInSerch': self.showInSerch,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [InfraTableFields.id,InfraTableFields.tableId,InfraTableFields.fieldName,InfraTableFields.isPrimaryKey,InfraTableFields.isAutoIncrement,InfraTableFields.canNull,InfraTableFields.dataType,InfraTableFields.description,InfraTableFields.length,InfraTableFields.showInTable,InfraTableFields.showInForm,InfraTableFields.showDetail,InfraTableFields.showInSerch]