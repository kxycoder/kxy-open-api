from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger,Text
from kxy.framework.base_entity import JSONString
from kxy.framework.filter import FilterTenant

# @FilterTenant()
class InfraTemplate(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'infra_template'

    id = Column('id',Integer, comment='模版编号',primary_key=True,autoincrement=True)
    name = Column('name',String(30), comment='模版名称')
    templateType = Column('template_type',String(5), comment='模板类型(ui-前端，api-后端)')
    variable = Column('variable',JSONString, comment='模版变量')
    baseCls = Column('base_cls',Text, comment='基类')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    # tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = []

    InsertOtherFields= ['name', 'variable','baseCls','templateType']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'templateType': self.templateType,
           'variable': self.variable,
           'baseCls': self.baseCls,
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
           'name': self.name,
            'templateType': self.templateType,
           'variable': self.variable,
           'baseCls': self.base_cls,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [InfraTemplate.id,InfraTemplate.name,InfraTemplate.templateType,InfraTemplate.variable]