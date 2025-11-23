from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class ProductBrowseHistory(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'product_browse_history'


    id = Column('id',Integer, comment='记录编号',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='用户编号')
    spuId = Column('spu_id',Integer, comment='商品 SPU 编号')
    userDeleted = Column('user_deleted',Integer, comment='用户是否删除')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')
    index = Column('INDEX',String(0), comment='INDEX')
    index = Column('INDEX',String(0), comment='INDEX')


    InsertRequireFields = ['userId', 'spuId', 'userDeleted']
    InsertOtherFields= ['index', 'index']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'spuId': self.spuId,
           'userDeleted': self.userDeleted,
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
           'spuId': self.spuId,
           'userDeleted': self.userDeleted,
           'index': self.index,
           'index': self.index,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [ProductBrowseHistory.id,ProductBrowseHistory.userId,ProductBrowseHistory.spuId,ProductBrowseHistory.userDeleted,ProductBrowseHistory.index,ProductBrowseHistory.index]