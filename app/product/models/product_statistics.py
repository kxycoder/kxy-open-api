from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class ProductStatistics(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'product_statistics'


    id = Column('id',Integer, comment='编号，主键自增',primary_key=True,autoincrement=True)
    time = Column('time',String(0), comment='统计日期')
    spuId = Column('spu_id',Integer, comment='商品 SPU 编号')
    browseCount = Column('browse_count',Integer, comment='浏览量')
    browseUserCount = Column('browse_user_count',Integer, comment='访客量')
    favoriteCount = Column('favorite_count',Integer, comment='收藏数量')
    cartCount = Column('cart_count',Integer, comment='加购数量')
    orderCount = Column('order_count',Integer, comment='下单件数')
    orderPayCount = Column('order_pay_count',Integer, comment='支付件数')
    orderPayPrice = Column('order_pay_price',Integer, comment='支付金额，单位：分')
    afterSaleCount = Column('after_sale_count',Integer, comment='退款件数')
    afterSaleRefundPrice = Column('after_sale_refund_price',Integer, comment='退款金额，单位：分')
    browseConvertPercent = Column('browse_convert_percent',Integer, comment='访客支付转化率（百分比）')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')
    index = Column('INDEX',String(0), comment='INDEX')
    index = Column('INDEX',String(0), comment='INDEX')


    InsertRequireFields = ['time', 'spuId', 'browseCount', 'browseUserCount', 'favoriteCount', 'cartCount', 'orderCount', 'orderPayCount', 'orderPayPrice', 'afterSaleCount', 'afterSaleRefundPrice', 'browseConvertPercent']
    InsertOtherFields= ['index', 'index']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'time': self.time.strftime("%Y-%m-%d %H:%M:%S") if self.time else None,
           'spuId': self.spuId,
           'browseCount': self.browseCount,
           'browseUserCount': self.browseUserCount,
           'favoriteCount': self.favoriteCount,
           'cartCount': self.cartCount,
           'orderCount': self.orderCount,
           'orderPayCount': self.orderPayCount,
           'orderPayPrice': self.orderPayPrice,
           'afterSaleCount': self.afterSaleCount,
           'afterSaleRefundPrice': self.afterSaleRefundPrice,
           'browseConvertPercent': self.browseConvertPercent,
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
           'time': self.time,
           'spuId': self.spuId,
           'browseCount': self.browseCount,
           'browseUserCount': self.browseUserCount,
           'favoriteCount': self.favoriteCount,
           'cartCount': self.cartCount,
           'orderCount': self.orderCount,
           'orderPayCount': self.orderPayCount,
           'orderPayPrice': self.orderPayPrice,
           'afterSaleCount': self.afterSaleCount,
           'afterSaleRefundPrice': self.afterSaleRefundPrice,
           'browseConvertPercent': self.browseConvertPercent,
           'index': self.index,
           'index': self.index,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [ProductStatistics.id,ProductStatistics.time,ProductStatistics.spuId,ProductStatistics.browseCount,ProductStatistics.browseUserCount,ProductStatistics.favoriteCount,ProductStatistics.cartCount,ProductStatistics.orderCount,ProductStatistics.orderPayCount,ProductStatistics.orderPayPrice,ProductStatistics.afterSaleCount,ProductStatistics.afterSaleRefundPrice,ProductStatistics.browseConvertPercent,ProductStatistics.index,ProductStatistics.index]