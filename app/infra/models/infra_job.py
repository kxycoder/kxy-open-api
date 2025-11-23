from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class InfraJob(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'infra_job'

    id = Column('id',Integer, comment='任务编号',primary_key=True,autoincrement=True)
    name = Column('name',String(32), comment='任务名称')
    status = Column('status',Integer, comment='任务状态')
    handlerName = Column('handler_name',String(64), comment='处理器的名字')
    handlerParam = Column('handler_param',String(255), comment='处理器的参数')
    cronExpression = Column('cron_expression',String(32), comment='CRON 表达式')
    retryCount = Column('retry_count',Integer, comment='重试次数')
    retryInterval = Column('retry_interval',Integer, comment='重试间隔')
    monitorTimeout = Column('monitor_timeout',Integer, comment='监控超时时间')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = ['status', 'retryCount', 'retryInterval', 'monitorTimeout']

    InsertOtherFields= ['name', 'handlerName', 'handlerParam', 'cronExpression']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'status': self.status,
           'handlerName': self.handlerName,
           'handlerParam': self.handlerParam,
           'cronExpression': self.cronExpression,
           'retryCount': self.retryCount,
           'retryInterval': self.retryInterval,
           'monitorTimeout': self.monitorTimeout,
           'creator': self.creator,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updater': self.updater,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'deleted': self.deleted,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'handlerName': self.handlerName,
           'handlerParam': self.handlerParam,
           'cronExpression': self.cronExpression,
           'retryCount': self.retryCount,
           'retryInterval': self.retryInterval,
           'monitorTimeout': self.monitorTimeout,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [InfraJob.id,InfraJob.name,InfraJob.handlerName,InfraJob.handlerParam,InfraJob.cronExpression,InfraJob.retryCount,InfraJob.retryInterval,InfraJob.monitorTimeout]