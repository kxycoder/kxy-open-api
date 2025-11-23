#!/usr/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from app.database import Base
from app.common.base_entity import BaseEntity

class PublicDictionary(BaseEntity, Base):
    __tablename__ = 'sys_public_dictionary'

    Id = Column(String(36), comment='',primary_key=True)
    SystemCode = Column(String(200), comment='')
    DicType = Column(String(45), comment='')
    Title = Column(String(225), comment='标题')
    Key = Column(String(45), comment='键')
    Value = Column(String(500), comment='值')
    Description = Column(String(225), comment='描述')
    Status = Column(Integer, comment='状态 (0-创建 5- 激活 10-删除)')
    ExData=Column(String(255),comment='扩展数据')
    CreateUser = Column(String(36), comment='创建人')
    CreateDate = Column(DateTime, comment='创建日期')
    LastModifiedUser = Column(String(36), comment='最后修改人')
    LastModifiedDate = Column(DateTime, comment='最后修改时间')
    Sort = Column(Integer, comment='排序')


    InsertRequireFields = []

    InsertOtherFields= ['Id', 'SystemCode', 'DicType','Title', 'Key', 'Value','ExData','Description','Status','Sort']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'Id': self.Id,
           'SystemCode': self.SystemCode,
           'DicType': self.DicType,
           'Title': self.Title,
           'Key': self.Key,
           'Value': self.Value,
           'ExData':self.ExData,
           'Description': self.Description,
           'Status': self.Status,
            'Sort': self.Sort,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
           'LastModifiedUser': self.LastModifiedUser,
           'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,

        }
        return resp_dict

    def getIdValue(self):
        return {
            'Key': int(self.Key),
            'Value': self.Value,
            'ExData':self.ExData,
        }
    def getKeyValue(self):    
        return {
            'Key': self.Key,
            'Value': self.Value,
            'ExData':self.ExData,
        }