from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant
from kxy.framework.base_entity import JSONString

@FilterTenant()
class TradeDeliveryExpressTemplateFree(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'trade_delivery_express_template_free'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    templateId = Column('template_id',Integer, comment='快递运费模板编号')
    areaIds = Column('area_ids',JSONString(0), comment='包邮区域 id')
    freePrice = Column('free_price',Integer, comment='包邮金额，单位：分')
    freeCount = Column('free_count',Integer, comment='包邮件数,')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['templateId', 'freePrice', 'freeCount']
    InsertOtherFields= ['areaIds']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'templateId': self.templateId,
           'areaIds': self.areaIds,
           'freePrice': self.freePrice,
           'freeCount': self.freeCount,
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
           'templateId': self.templateId,
           'areaIds': self.areaIds,
           'freePrice': self.freePrice,
           'freeCount': self.freeCount,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeDeliveryExpressTemplateFree.id,TradeDeliveryExpressTemplateFree.templateId,TradeDeliveryExpressTemplateFree.areaIds,TradeDeliveryExpressTemplateFree.freePrice,TradeDeliveryExpressTemplateFree.freeCount]