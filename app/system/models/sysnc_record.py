#!/usr/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from app.database import Base
from app.common.base_entity import BaseEntity

class SysncRecord(BaseEntity, Base):
    __tablename__ = 'sysnc_record'

    Id = Column(String(36), comment='',primary_key=True)
    SyncType = Column(String(20), comment='同步类型(1-menu)')
    SyncDate = Column(DateTime, comment='')
    SystemCode= Column(String(200), comment='SystemCode')
    Status = Column(Integer, comment='状态（0-同步中  5-同步成功  10-删除）')
    CreateUser = Column(String(36), comment='创建人')
    CreateDate = Column(DateTime, comment='')


    InsertRequireFields = []

    InsertOtherFields= ['Id', 'SyncType', 'SyncDate', 'Status']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
                       'Id': self.Id,
           'SyncType': self.SyncType,
           'SyncDate': self.SyncDate,
           'Status': self.Status,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,

        }
        return resp_dict