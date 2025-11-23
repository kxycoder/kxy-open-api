#!/usr/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from app.database import Base
from app.common.base_entity import BaseEntity

class OptSsoTokens(BaseEntity, Base):
    __tablename__ = 'sys_tokens'

    Token = Column(String(255), comment='',primary_key=True)
    UserId = Column(String(36), comment='')
    Expires = Column(DateTime, comment='')


    InsertRequireFields = []

    InsertOtherFields= ['Token', 'UserId', 'Expires']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
                       'Token': self.Token,
           'UserId': self.UserId,
           'Expires': self.Expires,

        }
        return resp_dict