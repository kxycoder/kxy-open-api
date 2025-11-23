from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class MemberLevel(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'member_level'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    name = Column('name',String(30), comment='等级名称')
    level = Column('level',Integer, comment='等级')
    experience = Column('experience',Integer, comment='升级经验')
    discountPercent = Column('discount_percent',Integer, comment='享受折扣')
    icon = Column('icon',String(255), comment='等级图标')
    backgroundUrl = Column('background_url',String(255), comment='等级背景图')
    status = Column('status',Integer, comment='状态')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['level', 'experience', 'discountPercent', 'status']
    InsertOtherFields= ['name', 'icon', 'backgroundUrl']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'level': self.level,
           'experience': self.experience,
           'discountPercent': self.discountPercent,
           'icon': self.icon,
           'backgroundUrl': self.backgroundUrl,
           'status': self.status,
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
           'name': self.name,
           'level': self.level,
           'experience': self.experience,
           'discountPercent': self.discountPercent,
           'icon': self.icon,
           'backgroundUrl': self.backgroundUrl,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [MemberLevel.id,MemberLevel.name,MemberLevel.level,MemberLevel.experience,MemberLevel.discountPercent,MemberLevel.icon,MemberLevel.backgroundUrl]