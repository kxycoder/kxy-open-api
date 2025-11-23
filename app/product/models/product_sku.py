from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant
from kxy.framework.base_entity import JSONString

@FilterTenant()
class ProductSku(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'product_sku'


    id = Column('id',Integer, comment='主键',primary_key=True,autoincrement=True)
    spuId = Column('spu_id',Integer, comment='spu编号')
    properties = Column('properties',JSONString(512), comment='属性数组，JSON 格式 [{propertId: , valueId: }, {propertId: , valueId: }]')
    price = Column('price',Integer, comment='商品价格，单位：分')
    marketPrice = Column('market_price',Integer, comment='市场价，单位：分')
    costPrice = Column('cost_price',Integer, comment='成本价，单位： 分')
    barCode = Column('bar_code',String(64), comment='SKU 的条形码')
    picUrl = Column('pic_url',String(256), comment='图片地址')
    stock = Column('stock',Integer, comment='库存')
    weight = Column('weight',String(0), comment='商品重量，单位：kg 千克')
    volume = Column('volume',String(0), comment='商品体积，单位：m^3 平米')
    firstBrokeragePrice = Column('first_brokerage_price',Integer, comment='一级分销的佣金，单位：分')
    secondBrokeragePrice = Column('second_brokerage_price',Integer, comment='二级分销的佣金，单位：分')
    salesCount = Column('sales_count',Integer, comment='商品销量')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    creator = Column('creator',String(64), comment='创建人')
    updater = Column('updater',String(0), comment='更新人')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['spuId', 'price', 'costPrice']
    InsertOtherFields= ['properties', 'marketPrice', 'barCode', 'picUrl', 'stock', 'weight', 'volume', 'firstBrokeragePrice', 'secondBrokeragePrice', 'salesCount']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'spuId': self.spuId,
           'properties': self.properties,
           'price': self.price,
           'marketPrice': self.marketPrice,
           'costPrice': self.costPrice,
           'barCode': self.barCode,
           'picUrl': self.picUrl,
           'stock': self.stock,
           'weight': self.weight,
           'volume': self.volume,
           'firstBrokeragePrice': self.firstBrokeragePrice,
           'secondBrokeragePrice': self.secondBrokeragePrice,
           'salesCount': self.salesCount,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'creator': self.creator,
           'updater': self.updater,
           'deleted': self.deleted,
           'tenantId': self.tenantId,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'spuId': self.spuId,
           'properties': self.properties,
           'price': self.price,
           'marketPrice': self.marketPrice,
           'costPrice': self.costPrice,
           'barCode': self.barCode,
           'picUrl': self.picUrl,
           'stock': self.stock,
           'weight': self.weight,
           'volume': self.volume,
           'firstBrokeragePrice': self.firstBrokeragePrice,
           'secondBrokeragePrice': self.secondBrokeragePrice,
           'salesCount': self.salesCount,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [ProductSku.id,ProductSku.spuId,ProductSku.properties,ProductSku.price,ProductSku.marketPrice,ProductSku.costPrice,ProductSku.barCode,ProductSku.picUrl,ProductSku.stock,ProductSku.weight,ProductSku.volume,ProductSku.firstBrokeragePrice,ProductSku.secondBrokeragePrice,ProductSku.salesCount]