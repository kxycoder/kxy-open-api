#!/usr/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from app.database import Base
from app.common.base_entity import BaseEntity

class MgRoleUser(BaseEntity, Base):
    __tablename__ = 'sys_role_user'

    Id = Column(String(36), comment='关系编号',primary_key=True)
    RoleId = Column(Integer, comment='角色Id')
    UserId = Column(String(32), comment='用户Id')
    CreateUser = Column(String(36), comment='创建人')
    CreateDate = Column(DateTime, comment='')
    LastModifiedUser = Column(String(36), comment='修改人')
    LastModifiedDate = Column(DateTime, comment='')


    InsertRequireFields = []

    InsertOtherFields= ['Id', 'RoleId', 'UserId']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
                       'Id': self.Id,
           'RoleId': self.RoleId,
           'UserId': self.UserId,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
           'LastModifiedUser': self.LastModifiedUser,
           'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,

        }
        return resp_dict