from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant
from kxy.framework.base_entity import JSONString

@FilterTenant()
class TradeDeliveryExpressTemplateCharge(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'trade_delivery_express_template_charge'


    id = Column('id',Integer, comment='编号，自增',primary_key=True,autoincrement=True)
    templateId = Column('template_id',Integer, comment='快递运费模板编号')
    areaIds = Column('area_ids',JSONString(0), comment='配送区域 id')
    chargeMode = Column('charge_mode',Integer, comment='配送计费方式')
    startCount = Column('start_count',String(0), comment='首件数量')
    startPrice = Column('start_price',Integer, comment='起步价，单位：分')
    extraCount = Column('extra_count',String(0), comment='续件数量')
    extraPrice = Column('extra_price',Integer, comment='额外价，单位：分')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['templateId', 'chargeMode', 'startCount', 'startPrice', 'extraCount', 'extraPrice']
    InsertOtherFields= ['areaIds']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'templateId': self.templateId,
           'areaIds': self.areaIds,
           'chargeMode': self.chargeMode,
           'startCount': self.startCount,
           'startPrice': self.startPrice,
           'extraCount': self.extraCount,
           'extraPrice': self.extraPrice,
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
           'chargeMode': self.chargeMode,
           'startCount': self.startCount,
           'startPrice': self.startPrice,
           'extraCount': self.extraCount,
           'extraPrice': self.extraPrice,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeDeliveryExpressTemplateCharge.id,TradeDeliveryExpressTemplateCharge.templateId,TradeDeliveryExpressTemplateCharge.areaIds,TradeDeliveryExpressTemplateCharge.chargeMode,TradeDeliveryExpressTemplateCharge.startCount,TradeDeliveryExpressTemplateCharge.startPrice,TradeDeliveryExpressTemplateCharge.extraCount,TradeDeliveryExpressTemplateCharge.extraPrice]