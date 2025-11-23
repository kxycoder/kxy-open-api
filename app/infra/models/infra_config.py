from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class InfraConfig(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'infra_config'

    id = Column('id',Integer, comment='参数主键',primary_key=True,autoincrement=True)
    category = Column('category',String(50), comment='参数分组')
    type = Column('type',Integer, comment='参数类型',default=2)
    name = Column('name',String(100), comment='参数名称')
    key = Column('config_key',String(100), comment='参数键名')
    value = Column('value',String(500), comment='参数键值')
    visible = Column('visible',Integer, comment='是否可见')
    remark = Column('remark',String(500), comment='备注')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = [ 'visible']

    InsertOtherFields= ['type','category', 'name', 'key', 'value', 'remark']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'category': self.category,
           'type': self.type,
           'name': self.name,
           'key': self.key,
           'value': self.value,
           'visible': self.visible,
           'remark': self.remark,
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
           'category': self.category,
           'type': self.type,
           'name': self.name,
           'key': self.key,
           'value': self.value,
           'visible': self.visible,
           'remark': self.remark,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [InfraConfig.id,InfraConfig.category,InfraConfig.type,InfraConfig.name,InfraConfig.key,InfraConfig.value,InfraConfig.visible,InfraConfig.remark]