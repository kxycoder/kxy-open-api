#!/usr/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from app.common.base_entity import BaseEntity
from app.database import Base

class BdArea(BaseEntity, Base):
    __tablename__ = 'sys_area'

    Id = Column(String(36), comment='编号',primary_key=True)
    Code = Column(String(12), comment='编码')
    JoinCode = Column(String(9), comment='内部编码')
    Name = Column(String(64), comment='名称')
    ParentId = Column(Integer, comment='父节点')
    Level = Column(Integer, comment='级别')


    InsertRequireFields = ['Id']

    InsertOtherFields= ['Code', 'JoinCode', 'Name', 'ParentId', 'Level']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
                       'Id': self.Id,
           'Code': self.Code,
           'JoinCode': self.JoinCode,
           'Name': self.Name,
           'ParentId': self.ParentId,
           'Level': self.Level,

        }
        return resp_dict