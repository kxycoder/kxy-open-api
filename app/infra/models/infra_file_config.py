from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger,Boolean
from kxy.framework.base_entity import JSONString
class InfraFileConfig(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'infra_file_config'

    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    name = Column('name',String(63), comment='配置名')
    storage = Column('storage',Integer, comment='存储器')
    remark = Column('remark',String(255), comment='备注')
    master = Column('master',Boolean, comment='是否为主配置')
    config = Column('config',JSONString(4096), comment='存储配置')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = ['storage', 'master']

    InsertOtherFields= ['name', 'remark', 'config']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'storage': self.storage,
           'remark': self.remark,
           'master': self.master,
           'config': self.config,
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
           'storage': self.storage,
           'remark': self.remark,
           'master': self.master,
           'config': self.config,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [InfraFileConfig.id,InfraFileConfig.name,InfraFileConfig.storage,InfraFileConfig.remark,InfraFileConfig.master,InfraFileConfig.config]