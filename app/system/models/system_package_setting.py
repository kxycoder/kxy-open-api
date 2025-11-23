

from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.base_entity import JSONString

class SystemPackageSetting(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'system_package_setting'


    id = Column('id',Integer, comment='模版编号',primary_key=True,autoincrement=True)
    packageId = Column('package_id',Integer, comment='套餐编号')
    categoryName = Column('category_name',Integer, comment='维度名称')
    ids = Column('ids',JSONString(500), comment='配置')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = ['packageId', 'categoryName']
    InsertOtherFields= ['ids']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'packageId': self.packageId,
           'categoryName': self.categoryName,
           'ids': self.ids,
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
           'packageId': self.packageId,
           'categoryName': self.categoryName,
           'ids': self.ids,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemPackageSetting.id,SystemPackageSetting.packageId,SystemPackageSetting.categoryName,SystemPackageSetting.ids]