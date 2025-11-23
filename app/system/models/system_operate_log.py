from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class SystemOperateLog(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_operate_log'

    id = Column('id',BigInteger, comment='日志主键',primary_key=True,autoincrement=True)
    traceId = Column('trace_id',String(64), comment='链路追踪编号')
    userId = Column('user_id',BigInteger, comment='用户编号')
    userType = Column('user_type',Integer, comment='用户类型')
    type = Column('type',String(50), comment='操作模块类型')
    subType = Column('sub_type',String(50), comment='操作名')
    bizId = Column('biz_id',BigInteger, comment='操作数据模块编号')
    action = Column('action',String(2000), comment='操作内容')
    success = Column('success',String(1), comment='操作结果')
    extra = Column('extra',String(2000), comment='拓展字段')
    requestMethod = Column('request_method',String(16), comment='请求方法名')
    requestUrl = Column('request_url',String(255), comment='请求地址')
    userIp = Column('user_ip',String(50), comment='用户 IP')
    userAgent = Column('user_agent',String(512), comment='浏览器 UA')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['userId', 'userType', 'bizId', 'success', 'tenantId']

    InsertOtherFields= ['traceId', 'type', 'subType', 'action', 'extra', 'requestMethod', 'requestUrl', 'userIp', 'userAgent']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'traceId': self.traceId,
           'userId': self.userId,
           'userType': self.userType,
           'type': self.type,
           'subType': self.subType,
           'bizId': self.bizId,
           'action': self.action,
           'success': self.success,
           'extra': self.extra,
           'requestMethod': self.requestMethod,
           'requestUrl': self.requestUrl,
           'userIp': self.userIp,
           'userAgent': self.userAgent,
           'creator': self.creator,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updater': self.updater,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'deleted': self.deleted,
           'tenantId': self.tenantId,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'traceId': self.traceId,
           'userId': self.userId,
           'userType': self.userType,
           'type': self.type,
           'subType': self.subType,
           'bizId': self.bizId,
           'action': self.action,
           'success': self.success,
           'extra': self.extra,
           'requestMethod': self.requestMethod,
           'requestUrl': self.requestUrl,
           'userIp': self.userIp,
           'userAgent': self.userAgent,
           'tenantId': self.tenantId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemOperateLog.id,SystemOperateLog.traceId,SystemOperateLog.userId,SystemOperateLog.userType,SystemOperateLog.type,SystemOperateLog.subType,SystemOperateLog.bizId,SystemOperateLog.action,SystemOperateLog.success,SystemOperateLog.extra,SystemOperateLog.requestMethod,SystemOperateLog.requestUrl,SystemOperateLog.userIp,SystemOperateLog.userAgent,SystemOperateLog.tenantId]