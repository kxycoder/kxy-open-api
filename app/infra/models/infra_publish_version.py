

from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger


class InfraPublishVersion(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'infra_publish_version'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    appName = Column('app_name',String(255), comment='应用名称')
    preVersion = Column('pre_version',String(255), comment='前一个版本')
    version = Column('version',String(255), comment='版本号')
    versionType = Column('version_type',String(10), comment='版本类型(normal，date)')
    version1 = Column('version1',Integer, comment='版本号第一位')
    version2 = Column('version2',Integer, comment='版本号第二位')
    version3 = Column('version3',Integer, comment='版本号第三位')
    version4 = Column('version4',Integer, comment='版本号第四位')
    status = Column('status',Integer, comment='任务状态')
    result = Column('result',String(4000), comment='结果数据')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = ['appName', 'status']
    InsertOtherFields= ['preVersion', 'version', 'versionType', 'version1', 'version2', 'version3', 'version4', 'result']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'appName': self.appName,
           'preVersion': self.preVersion,
           'version': self.version,
           'versionType': self.versionType,
           'version1': self.version1,
           'version2': self.version2,
           'version3': self.version3,
           'version4': self.version4,
           'status': self.status,
           'result': self.result,
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
           'appName': self.appName,
           'preVersion': self.preVersion,
           'version': self.version,
           'versionType': self.versionType,
           'version1': self.version1,
           'version2': self.version2,
           'version3': self.version3,
           'version4': self.version4,
           'result': self.result,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [InfraPublishVersion.id,InfraPublishVersion.appName,InfraPublishVersion.preVersion,InfraPublishVersion.version,InfraPublishVersion.versionType,InfraPublishVersion.version1,InfraPublishVersion.version2,InfraPublishVersion.version3,InfraPublishVersion.version4,InfraPublishVersion.result]