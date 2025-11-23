from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.base_entity import JSONString
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class InfraTable(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'infra_table'

    id = Column('id',Integer, comment='Id',primary_key=True,autoincrement=True)
    primaryKey = Column('primary_key',String(255), comment='主键')
    databaseName = Column('database_name',String(255), comment='数据库名')
    tableName = Column('table_name',String(255), comment='表名')
    tableDes = Column('table_des',String(255), comment='表描述')
    downUrl = Column('down_url',String(255), comment='下载链接')
    templateId = Column('template_id',Integer, comment='模板编号')
    templateParam = Column('template_param',JSONString, comment='模板参数')
    userId = Column('user_id',Integer, comment='用户编号')
    pageType = Column('page_type',String(255), comment='子表模式',default='single')
    parentId = Column('parent_id',Integer, comment='父表编号',default=0)
    childrenField = Column('children_field',String(100), comment='子级字段')
    subJoinMany = Column('sub_join_many',Integer, comment='主表与子表是否一对多',default=1)
    treeParentColumn = Column('tree_parent_column',String(100), comment='树表的父字段')
    treeNameColumn = Column('tree_name_column',String(100), comment='树表的名字字段')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = []

    InsertOtherFields= ['primaryKey', 'databaseName', 'tableName', 'tableDes', 'downUrl', 'templateId', 'templateParam', 'userId','parentId','childrenField','pageType','subJoinMany','treeParentColumn','treeNameColumn']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'primaryKey': self.primaryKey,
           'databaseName': self.databaseName,
           'tableName': self.tableName,
           'tableDes': self.tableDes,
           'downUrl': self.downUrl,
           'templateId': self.templateId,
           'templateParam': self.templateParam,
           'userId': self.userId,
           'parentId': self.parentId,
           'childrenField': self.childrenField,
           'pageType':self.pageType,
            'subJoinMany':self.subJoinMany,
            'treeParentColumn':self.treeParentColumn,
            'treeNameColumn':self.treeNameColumn,
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
            'primaryKey': self.primaryKey,
            'databaseName': self.databaseName,
            'tableName': self.tableName,
            'tableDes': self.tableDes,
            'downUrl': self.downUrl,
            'templateId': self.templateId,
            'templateParam': self.templateParam,
            'userId': self.userId,
            'parentId': self.parentId,
            'childrenField': self.childrenField,
            'pageType':self.pageType,
            'subJoinMany':self.subJoinMany,
            'treeParentColumn':self.treeParentColumn,
            'treeNameColumn':self.treeNameColumn,
        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [InfraTable.id,InfraTable.primaryKey,InfraTable.databaseName,InfraTable.tableName,InfraTable.tableDes,InfraTable.downUrl,InfraTable.templateId,InfraTable.templateParam,InfraTable.userId,InfraTable.parentId,InfraTable.childrenField,InfraTable.pageType,InfraTable.subJoinMany,InfraTable.treeParentColumn,InfraTable.treeNameColumn]