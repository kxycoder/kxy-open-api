# coding=UTF-8

import asyncio
from typing import Generic, TypeVar
from kxy.framework.base_dal import BaseDal as kxyBaseDal
from kxy.framework.base_config import BaseConfig as kxyBaseConfig
from kxy.framework.context import current_tenant_id
from sqlalchemy.ext.asyncio import AsyncSession

kxyBaseConfig.BussinessLog = False
BaseDal = kxyBaseDal

MyBaseDal = kxyBaseDal
MyBaseDal._id_field = 'id'
MyBaseDal._status_field = 'status'
MyBaseDal._createUser_field = 'creator'
MyBaseDal._createDate_field = 'createTime'
MyBaseDal._lastModifiedUser_Field = 'updater'
MyBaseDal._lastModifiedDate_Field = 'updateTime'
MyBaseDal._isDelete_field = 'deleted'
MyBaseDal._uid_field = 'user_id'

