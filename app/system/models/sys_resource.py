#!/usr/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from app.database import Base
from app.common.base_entity import BaseEntity

class MgResource(BaseEntity, Base):
    __tablename__ = 'sys_resource'

    Id = Column(String(36), comment='资源Id',primary_key=True)
    MenuId = Column(Integer, comment='菜单Id')
    Name = Column(String(255), comment='资源名称')
    Schema = Column(String(32), comment='权限标识')
    Description = Column(String(255), comment='资源描述')
    CreateUser = Column(String(36), comment='创建人')
    CreateDate = Column(DateTime, comment='')
    LastModifiedUser = Column(String(36), comment='修改人')
    LastModifiedDate = Column(DateTime, comment='')


    InsertRequireFields = []

    InsertOtherFields= ['Id', 'MenuId', 'Name', 'Schema', 'Description']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'Id': self.Id,
           'MenuId': self.MenuId,
           'Name': self.Name,
           'Schema': self.Schema,
           'Description': self.Description,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
           'LastModifiedUser': self.LastModifiedUser,
           'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None

        }
        return resp_dict