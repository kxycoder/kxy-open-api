from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class MemberSignInRecord(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'member_sign_in_record'


    id = Column('id',Integer, comment='签到自增id',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='签到用户')
    day = Column('day',Integer, comment='第几天签到')
    point = Column('point',Integer, comment='签到的分数')
    experience = Column('experience',Integer, comment='奖励经验')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['point', 'experience']
    InsertOtherFields= ['userId', 'day']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'day': self.day,
           'point': self.point,
           'experience': self.experience,
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
           'userId': self.userId,
           'day': self.day,
           'point': self.point,
           'experience': self.experience,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [MemberSignInRecord.id,MemberSignInRecord.userId,MemberSignInRecord.day,MemberSignInRecord.point,MemberSignInRecord.experience]