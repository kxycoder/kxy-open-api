from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class MemberExperienceRecord(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'member_experience_record'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='用户编号')
    bizId = Column('biz_id',String(64), comment='业务编号')
    bizType = Column('biz_type',Integer, comment='业务类型')
    title = Column('title',String(30), comment='标题')
    description = Column('description',String(512), comment='描述')
    experience = Column('experience',Integer, comment='经验')
    totalExperience = Column('total_experience',Integer, comment='变更后的经验')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')
    index = Column('INDEX',String(0), comment='会员经验记录-用户编号')
    index = Column('INDEX',String(0), comment='INDEX')


    InsertRequireFields = ['userId', 'bizType', 'experience', 'totalExperience']
    InsertOtherFields= ['bizId', 'title', 'description', 'index', 'index']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'bizId': self.bizId,
           'bizType': self.bizType,
           'title': self.title,
           'description': self.description,
           'experience': self.experience,
           'totalExperience': self.totalExperience,
           'creator': self.creator,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updater': self.updater,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'deleted': self.deleted,
           'tenantId': self.tenantId,
           'index': self.index,
           'index': self.index,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'bizId': self.bizId,
           'bizType': self.bizType,
           'title': self.title,
           'description': self.description,
           'experience': self.experience,
           'totalExperience': self.totalExperience,
           'index': self.index,
           'index': self.index,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [MemberExperienceRecord.id,MemberExperienceRecord.userId,MemberExperienceRecord.bizId,MemberExperienceRecord.bizType,MemberExperienceRecord.title,MemberExperienceRecord.description,MemberExperienceRecord.experience,MemberExperienceRecord.totalExperience,MemberExperienceRecord.index,MemberExperienceRecord.index]