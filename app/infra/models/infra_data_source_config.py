from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class InfraDataSourceConfig(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'infra_data_source_config'

    id = Column('id',Integer, comment='主键编号',primary_key=True,autoincrement=True)
    name = Column('name',String(100), comment='参数名称')
    url = Column('url',String(1024), comment='数据源连接')
    username = Column('username',String(255), comment='用户名')
    password = Column('password',String(255), comment='密码')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = []

    InsertOtherFields= ['name', 'url', 'username', 'password']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'url': self.url,
           'username': self.username,
           'password': self.password,
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
           'url': self.url,
           'username': self.username,
           'password': self.password,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [InfraDataSourceConfig.id,InfraDataSourceConfig.name,InfraDataSourceConfig.url,InfraDataSourceConfig.username,InfraDataSourceConfig.password]