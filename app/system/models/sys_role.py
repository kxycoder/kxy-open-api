#!/usr/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from app.database import Base
from app.common.base_entity import BaseEntity

class MgRole(BaseEntity, Base):
    __tablename__ = 'sys_role'

    Id = Column(String(36), comment='角色Id',primary_key=True)
    Name = Column(String(255), comment='角色名称')
    Description = Column(String(255), comment='角色描述')
    SystemCode = Column(String(255), comment='系统标识')
    CreateUser = Column(String(36), comment='创建人')
    CreateDate = Column(DateTime, comment='')
    LastModifiedUser = Column(String(36), comment='修改人')
    LastModifiedDate = Column(DateTime, comment='')

    InsertRequireFields = []

    InsertOtherFields= ['Id', 'Name', 'Description', 'SystemCode']        

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
                       'Id': self.Id,
           'Name': self.Name,
           'Description': self.Description,
           'SystemCode': self.SystemCode,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
           'LastModifiedUser': self.LastModifiedUser,
           'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,
        }
        return resp_dict