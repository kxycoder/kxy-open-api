from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class InfraFile(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'infra_file'

    id = Column('id',Integer, comment='文件编号',primary_key=True,autoincrement=True)
    configId = Column('config_id',BigInteger, comment='配置编号')
    name = Column('name',String(256), comment='文件名')
    path = Column('path',String(512), comment='文件路径')
    url = Column('url',String(1024), comment='文件 URL')
    type = Column('type',String(128), comment='文件类型')
    size = Column('size',Integer, comment='文件大小')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = ['size']

    InsertOtherFields= ['configId', 'name', 'path', 'url', 'type']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'configId': self.configId,
           'name': self.name,
           'path': self.path,
           'url': self.url,
           'type': self.type,
           'size': self.size,
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
           'configId': self.configId,
           'name': self.name,
           'path': self.path,
           'url': self.url,
           'type': self.type,
           'size': self.size,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [InfraFile.id,InfraFile.configId,InfraFile.name,InfraFile.path,InfraFile.url,InfraFile.type,InfraFile.size]