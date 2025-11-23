from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class SystemSmsCode(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_sms_code'

    id = Column('id',BigInteger, comment='编号',primary_key=True,autoincrement=True)
    mobile = Column('mobile',String(11), comment='手机号')
    code = Column('code',String(6), comment='验证码')
    createIp = Column('create_ip',String(15), comment='创建 IP')
    scene = Column('scene',Integer, comment='发送场景')
    todayIndex = Column('today_index',Integer, comment='今日发送的第几条')
    used = Column('used',Integer, comment='是否使用')
    usedTime = Column('used_time',DateTime, comment='使用时间')
    usedIp = Column('used_ip',String(255), comment='使用 IP')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['scene', 'todayIndex', 'used', 'tenantId']

    InsertOtherFields= ['mobile', 'code', 'createIp', 'usedTime', 'usedIp']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'mobile': self.mobile,
           'code': self.code,
           'createIp': self.createIp,
           'scene': self.scene,
           'todayIndex': self.todayIndex,
           'used': self.used,
           'usedTime': self.usedTime.strftime("%Y-%m-%d %H:%M:%S") if self.usedTime else None,
           'usedIp': self.usedIp,
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
           'mobile': self.mobile,
           'code': self.code,
           'createIp': self.createIp,
           'scene': self.scene,
           'todayIndex': self.todayIndex,
           'used': self.used,
           'usedTime': self.usedTime,
           'usedIp': self.usedIp,
           'tenantId': self.tenantId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemSmsCode.id,SystemSmsCode.mobile,SystemSmsCode.code,SystemSmsCode.createIp,SystemSmsCode.scene,SystemSmsCode.todayIndex,SystemSmsCode.used,SystemSmsCode.usedTime,SystemSmsCode.usedIp,SystemSmsCode.tenantId]