from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class MemberPointRecord(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'member_point_record'


    id = Column('id',Integer, comment='自增主键',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='用户编号')
    bizId = Column('biz_id',String(255), comment='业务编码')
    bizType = Column('biz_type',Integer, comment='业务类型')
    title = Column('title',String(255), comment='积分标题')
    description = Column('description',String(5000), comment='积分描述')
    point = Column('point',Integer, comment='积分')
    totalPoint = Column('total_point',Integer, comment='变动后的积分')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')
    index = Column('INDEX',String(0), comment='INDEX')
    index = Column('INDEX',String(0), comment='INDEX')


    InsertRequireFields = ['userId', 'bizType', 'point', 'totalPoint']
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
           'point': self.point,
           'totalPoint': self.totalPoint,
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
           'point': self.point,
           'totalPoint': self.totalPoint,
           'index': self.index,
           'index': self.index,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [MemberPointRecord.id,MemberPointRecord.userId,MemberPointRecord.bizId,MemberPointRecord.bizType,MemberPointRecord.title,MemberPointRecord.description,MemberPointRecord.point,MemberPointRecord.totalPoint,MemberPointRecord.index,MemberPointRecord.index]