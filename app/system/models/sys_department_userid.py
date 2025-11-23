#!/usr/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, TEXT
from app.database import Base
from app.common.base_entity import BaseEntity


class DepartmentUserid(BaseEntity, Base):
    __tablename__ = 'sys_department_userid'

    Id = Column(String(36), comment='', primary_key=True)
    DepartmentId = Column(Integer, comment='')
    DepartmentName = Column(String(45), comment='部门名称')
    UserId = Column(Integer, comment='')
    UserName = Column(String(20), comment='')
    Leader = Column(Integer, comment='直接上级')
    UserType = Column(Integer, comment='用户类型（1-正常 0-虚拟组）')
    Position = Column(Integer, comment='岗位编号')
    Function = Column(String(45), comment='职能')
    Status = Column(Integer, comment='状态（1-生效，10-删除）')
    CreateUserName = Column(String(20), comment='创建用户名')
    CreateUser = Column(String(20), comment='创建用户')
    CreateDate = Column(DateTime, comment='创建时间')
    LastModifiedUser = Column(String(20), comment='最后修改用户')
    LastModifiedDate = Column(DateTime, comment='最后修改时间')
    PhoneNumber = Column(String(45), comment='')
    Email = Column(String(45), comment='邮箱')
    QYWXUserId = Column(String(45), comment='企业微信用户编号')
    UserRole = Column(Integer, comment='0-员工    10- 主管   20-部门负责人   50-CTO')
    IsLeader = Column(Integer, comment='上级字段，标识是否为上级。0表示普通成员，1表示上级')
    Sex = Column(Integer, comment='性别')
    VpnId = Column(Integer, comment='VPN账号ID')

    InsertRequireFields = []

    InsertOtherFields = ['Id', 'DepartmentId', 'DepartmentName', 'UserId', 'UserName', 'Leader', 'UserType', 'Position',
                         'Function', 'Status', 'CreateUserName', 'PhoneNumber', 'Email', 'QYWXUserId', 'UserRole',
                         'IsLeader', 'Sex', 'VpnId']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
            'Id': self.Id,
            'DepartmentId': self.DepartmentId,
            'DepartmentName': self.DepartmentName,
            'UserId': self.UserId,
            'UserName': self.UserName,
            'Leader': self.Leader,
            'UserType': self.UserType,
            'Position': self.Position,
            'Function': self.Function,
            'Status': self.Status,
            'CreateUserName': self.CreateUserName,
            'CreateUser': self.CreateUser,
            'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
            'LastModifiedUser': self.LastModifiedUser,
            'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,
            'PhoneNumber': self.PhoneNumber,
            'Email': self.Email,
            'QYWXUserId': self.QYWXUserId,
            'UserRole': self.UserRole,
            'IsLeader': self.IsLeader,
            'Sex': self.Sex,
            'VpnId': self.VpnId
        }
        return resp_dict
