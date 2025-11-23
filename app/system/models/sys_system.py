#!/usr/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from app.database import Base
from app.common.base_entity import BaseEntity

class MgSystem(BaseEntity, Base):
    __tablename__ = 'sys_system'

    Id = Column(String(36), comment='系统Id',primary_key=True)
    Name = Column(String(255), comment='系统名称')
    SystemCode = Column(String(32), comment='系统标识')
    Description = Column(String(255), comment='描述')
    CreateUser = Column(String(36), comment='')
    CreateDate = Column(DateTime, comment='')
    LastModifiedUser = Column(String(36), comment='')
    LastModifiedDate = Column(DateTime, comment='')
    Status = Column(Integer, comment='状态')


    InsertRequireFields = []

    InsertOtherFields= ['Id', 'Name', 'SystemCode', 'Description']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
            'Id': self.Id,
           'Name': self.Name,
           'SystemCode': self.SystemCode,
           'Description': self.Description,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
           'LastModifiedUser': self.LastModifiedUser,
           'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,

        }
        return resp_dict