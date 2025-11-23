#!/usr/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from app.database import Base
from app.common.base_entity import BaseEntity

class DepartmentInfo(BaseEntity, Base):
    __tablename__ = 'sys_department_info'

    Id = Column(String(36), comment='部门编号',primary_key=True)
    Name = Column(String(45), comment='')
    ParentId = Column(Integer, comment='父级部门')
    Leve = Column(Integer, comment='')
    Function = Column(Integer, comment='职能')
    PrincipalUserId = Column(Integer, comment='负责人')
    PrincipalUserName = Column(String(45), comment='负责人姓名')
    Status = Column(Integer, comment='状态（1-生效，10-删除）')
    CreateUserName = Column(String(20), comment='创建用户名')
    CreateUser = Column(String(20), comment='创建用户')
    CreateDate = Column(DateTime, comment='创建时间')
    LastModifiedUser = Column(String(20), comment='最后修改用户')
    LastModifiedDate = Column(DateTime, comment='最后修改时间')
    ChildIds = Column(String(200), comment='')
    Position = Column(Integer, comment='岗位')
    UserId = None
    UserName = None
    DepType = Column(String(10), comment='部门类型:group-组;dep-部门;center-中心级部门')


    InsertRequireFields = []

    InsertOtherFields= ['Id', 'Name', 'ParentId', 'Leve', 'PrincipalUserId', 'PrincipalUserName', 'Status',
                        'CreateUserName', 'ChildIds','Position', "DepType"]

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
            'Id': self.Id,
            'Name': self.Name,
            'ParentId': self.ParentId,
            'Leve': self.Leve,
            'PrincipalUserId': self.PrincipalUserId,
            'PrincipalUserName': self.PrincipalUserName,
            'Status': self.Status,
            'CreateUserName': self.CreateUserName,
            'CreateUser': self.CreateUser,
            'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
            'LastModifiedUser': self.LastModifiedUser,
            'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,
            'ChildIds': self.ChildIds,
            'Position': self.Position,
            'UserId': self.UserId,
            'UserName': self.UserName,
            'DepType': self.DepType
        }
        return resp_dict
