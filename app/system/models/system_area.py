from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class SystemArea(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int')
    __tablename__ = 'system_area'

    id = Column('id',Integer, comment='编号',primary_key=True)
    name = Column('name',String(30), comment='名称')
    type = Column('type',Integer, comment='类型(1-国家 2-省 3-市 4-区)')
    parentId = Column('parent_id',Integer, comment='父对象')
    status = Column('status',Integer, comment='状态（0正常 1停用）')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = ['status']

    InsertOtherFields= ['name', 'type', 'parentId']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'type': self.type,
           'parentId': self.parentId,
           'status': self.status,
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
           'type': self.type,
           'parentId': self.parentId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemArea.id,SystemArea.name,SystemArea.type,SystemArea.parentId]