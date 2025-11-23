from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class SystemLoginLog(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_login_log'

    id = Column('id',BigInteger, comment='访问ID',primary_key=True,autoincrement=True)
    logType = Column('log_type',BigInteger, comment='日志类型')
    traceId = Column('trace_id',String(64), comment='链路追踪编号')
    userId = Column('user_id',BigInteger, comment='用户编号')
    userType = Column('user_type',Integer, comment='用户类型')
    username = Column('username',String(50), comment='用户账号')
    result = Column('result',Integer, comment='登陆结果')
    userIp = Column('user_ip',String(50), comment='用户 IP')
    userAgent = Column('user_agent',String(512), comment='浏览器 UA')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = []

    InsertOtherFields= ['traceId', 'username', 'userIp', 'userAgent','logType', 'userId', 'userType', 'result', 'tenantId']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'logType': self.logType,
           'traceId': self.traceId,
           'userId': self.userId,
           'userType': self.userType,
           'username': self.username,
           'result': self.result,
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
           'logType': self.logType,
           'traceId': self.traceId,
           'userId': self.userId,
           'userType': self.userType,
           'username': self.username,
           'result': self.result,
           'userIp': self.userIp,
           'userAgent': self.userAgent,
           'tenantId': self.tenantId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemLoginLog.id,SystemLoginLog.logType,SystemLoginLog.traceId,SystemLoginLog.userId,SystemLoginLog.userType,SystemLoginLog.username,SystemLoginLog.result,SystemLoginLog.userIp,SystemLoginLog.userAgent,SystemLoginLog.tenantId]