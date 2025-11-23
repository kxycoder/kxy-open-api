from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class KxyDemo03Student(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'kxy_demo03_student'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    name = Column('name',String(100), comment='名字')
    sex = Column('sex',Integer, comment='性别')
    birthday = Column('birthday',DateTime, comment='出生日期')
    description = Column('description',String(255), comment='简介')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['sex', 'birthday']
    InsertOtherFields= ['name', 'description']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'sex': self.sex,
           'birthday': self.birthday.strftime("%Y-%m-%d %H:%M:%S") if self.birthday else None,
           'description': self.description,
           'creator': self.creator,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updater': self.updater,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'deleted': self.deleted,
           'tenantId': self.tenantId,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'sex': self.sex,
           'birthday': self.birthday,
           'description': self.description,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [KxyDemo03Student.id,KxyDemo03Student.name,KxyDemo03Student.sex,KxyDemo03Student.birthday,KxyDemo03Student.description]