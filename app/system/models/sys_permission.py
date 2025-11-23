#!/usr/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from app.database import Base
from app.common.base_entity import BaseEntity

class MgPermission(BaseEntity, Base):
    __tablename__ = 'sys_permission'

    Id = Column(String(36), comment='权限Id',primary_key=True)
    SystemCode = Column(String(32), comment='系统标识')
    ObjectId = Column(String(36), comment='对象Id')
    ObjectType = Column(String(16), comment='对象类型,Role:角色,User:用户')
    MenuSchema = Column(String(32), comment='菜单权限标识')
    ResourceSchema = Column(String(32), comment='资源权限标识')
    IsEnable = Column(String(1), comment='是否可用')
    IsVisible = Column(String(1), comment='是否可见')
    CreateUser = Column(String(36), comment='')
    CreateDate = Column(DateTime, comment='')
    LastModifiedUser = Column(String(36), comment='')
    LastModifiedDate = Column(DateTime, comment='')


    InsertRequireFields = []

    InsertOtherFields= ['Id', 'SystemCode', 'ObjectId', 'ObjectType', 'MenuSchema', 'ResourceSchema', 'IsEnable', 'IsVisible']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
                       'Id': self.Id,
           'SystemCode': self.SystemCode,
           'ObjectId': self.ObjectId,
           'ObjectType': self.ObjectType,
           'MenuSchema': self.MenuSchema,
           'ResourceSchema': self.ResourceSchema,
           'IsEnable': self.IsEnable,
           'IsVisible': self.IsVisible,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
           'LastModifiedUser': self.LastModifiedUser,
           'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,

        }
        return resp_dict