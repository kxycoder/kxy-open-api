from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class InfraJobLog(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'infra_job_log'

    id = Column('id',Integer, comment='日志编号',primary_key=True,autoincrement=True)
    jobId = Column('job_id',Integer, comment='任务编号')
    handlerName = Column('handler_name',String(64), comment='处理器的名字')
    handlerParam = Column('handler_param',String(255), comment='处理器的参数')
    executeIndex = Column('execute_index',Integer, comment='第几次执行')
    beginTime = Column('begin_time',DateTime, comment='开始执行时间')
    endTime = Column('end_time',DateTime, comment='结束执行时间')
    duration = Column('duration',Integer, comment='执行时长')
    status = Column('status',Integer, comment='任务状态')
    result = Column('result',String(4000), comment='结果数据')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = ['jobId', 'executeIndex', 'beginTime', 'status']

    InsertOtherFields= ['handlerName', 'handlerParam', 'endTime', 'duration', 'result']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'jobId': self.jobId,
           'handlerName': self.handlerName,
           'handlerParam': self.handlerParam,
           'executeIndex': self.executeIndex,
           'beginTime': self.beginTime.strftime("%Y-%m-%d %H:%M:%S") if self.beginTime else None,
           'endTime': self.endTime.strftime("%Y-%m-%d %H:%M:%S") if self.endTime else None,
           'duration': self.duration,
           'status': self.status,
           'result': self.result,
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
           'jobId': self.jobId,
           'handlerName': self.handlerName,
           'handlerParam': self.handlerParam,
           'executeIndex': self.executeIndex,
           'beginTime': self.beginTime,
           'endTime': self.endTime,
           'duration': self.duration,
           'result': self.result,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [InfraJobLog.id,InfraJobLog.jobId,InfraJobLog.handlerName,InfraJobLog.handlerParam,InfraJobLog.executeIndex,InfraJobLog.beginTime,InfraJobLog.endTime,InfraJobLog.duration,InfraJobLog.result]