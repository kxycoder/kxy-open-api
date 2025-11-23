#!/usr/bin/python
# -*- coding:utf-8 -*-
# from flask_sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy import Table, Column, Integer, String, DateTime
from app.database import Base
from app.common.base_entity import BaseEntity

class MgMenu(BaseEntity, Base):
    __tablename__ = 'sys_menu'

    Id = Column(String(36), comment='菜单Id',primary_key=True)
    SystemCode = Column(String(32), comment='系统标识')
    ParentId = Column(String(36), comment='上级菜单Id')
    Name = Column(String(255), comment='菜单名称')
    Description = Column(String(255), comment='描述')
    Schema = Column(String(32), comment='权限标识')
    RouteUrl = Column(String(255), comment='路由地址')
    NavigateUrl = Column(String(255), comment='菜单地址')
    Target = Column(String(16), comment='打开方式')
    IconUrl = Column(String(255), comment='图标地址')
    Sort = Column(Integer, comment='顺序')
    IsDisplay = Column(String(1), comment='是否显示')
    CreateUser = Column(String(36), comment='')
    CreateDate = Column(DateTime, comment='')
    LastModifiedUser = Column(String(36), comment='')
    LastModifiedDate = Column(DateTime, comment='')
    Component = Column(String(255), comment='组件地址')
    ComponentName = Column(String(255), comment='组件名称')
    Children = []
    Actions = []


    InsertRequireFields = []

    InsertOtherFields= ['Id', 'SystemCode', 'ParentId', 'Name', 'Description', 'Schema', 'RouteUrl', 'NavigateUrl', 'Target', 'IconUrl', 'Sort', 'IsDisplay']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'Id': self.Id,
           'SystemCode': self.SystemCode,
           'ParentId': self.ParentId,
           'Name': self.Name,
           'Description': self.Description,
           'Schema': self.Schema,
           'RouteUrl': self.RouteUrl,
           'NavigateUrl': self.NavigateUrl,
           'Target': self.Target,
           'IconUrl': self.IconUrl,
           'Sort': self.Sort,
           'IsDisplay': self.IsDisplay,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
           'LastModifiedUser': self.LastModifiedUser,
           'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,

        }
        return resp_dict
    def to_basic_dict_lower(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.Id,
           'parentId': self.ParentId,
           'name': self.Name,
           'component':self.Component,
           'componentName':self.ComponentName,
           'path': self.RouteUrl,
           'icon': self.IconUrl,
           'sort': self.Sort,
           'visible': self.IsDisplay=='1',
           "keepAlive": True,
           "alwaysShow": True,
           'actions': self.Actions,
        }
        return resp_dict