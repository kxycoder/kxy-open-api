from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant
from kxy.framework.base_entity import JSONString

@FilterTenant()
class TradeOrderItem(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'trade_order_item'


    id = Column('id',Integer, comment='订单项编号',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='用户编号')
    orderId = Column('order_id',Integer, comment='订单编号')
    cartId = Column('cart_id',Integer, comment='购物车项编号')
    spuId = Column('spu_id',Integer, comment='商品 SPU 编号')
    spuName = Column('spu_name',String(255), comment='商品 SPU 名称')
    skuId = Column('sku_id',Integer, comment='商品 SKU 编号')
    properties = Column('properties',JSONString(2000), comment='商品属性数组，JSON 格式')
    picUrl = Column('pic_url',String(200), comment='商品图片')
    count = Column('count',Integer, comment='购买数量')
    commentStatus = Column('comment_status',Integer, comment='是否评价')
    price = Column('price',Integer, comment='商品原价（单），单位：分')
    discountPrice = Column('discount_price',Integer, comment='商品级优惠（总），单位：分')
    deliveryPrice = Column('delivery_price',Integer, comment='运费金额，单位：分')
    adjustPrice = Column('adjust_price',Integer, comment='订单调价（总），单位：分')
    payPrice = Column('pay_price',Integer, comment='子订单实付金额（总），不算主订单分摊金额，单位：分')
    couponPrice = Column('coupon_price',Integer, comment='优惠劵减免金额，单位：分')
    pointPrice = Column('point_price',Integer, comment='积分抵扣的金额')
    usePoint = Column('use_point',Integer, comment='使用的积分')
    givePoint = Column('give_point',Integer, comment='赠送的积分')
    vipPrice = Column('vip_price',Integer, comment='VIP 减免金额，单位：分')
    afterSaleId = Column('after_sale_id',Integer, comment='售后订单编号')
    afterSaleStatus = Column('after_sale_status',Integer, comment='售后状态')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['count', 'commentStatus', 'price', 'discountPrice', 'deliveryPrice', 'adjustPrice', 'payPrice', 'couponPrice', 'pointPrice', 'usePoint', 'givePoint', 'vipPrice', 'afterSaleStatus']
    InsertOtherFields= ['userId', 'orderId', 'cartId', 'spuId', 'spuName', 'skuId', 'properties', 'picUrl', 'afterSaleId']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'orderId': self.orderId,
           'cartId': self.cartId,
           'spuId': self.spuId,
           'spuName': self.spuName,
           'skuId': self.skuId,
           'properties': self.properties,
           'picUrl': self.picUrl,
           'count': self.count,
           'commentStatus': self.commentStatus,
           'price': self.price,
           'discountPrice': self.discountPrice,
           'deliveryPrice': self.deliveryPrice,
           'adjustPrice': self.adjustPrice,
           'payPrice': self.payPrice,
           'couponPrice': self.couponPrice,
           'pointPrice': self.pointPrice,
           'usePoint': self.usePoint,
           'givePoint': self.givePoint,
           'vipPrice': self.vipPrice,
           'afterSaleId': self.afterSaleId,
           'afterSaleStatus': self.afterSaleStatus,
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
           'orderId': self.orderId,
           'cartId': self.cartId,
           'spuId': self.spuId,
           'spuName': self.spuName,
           'skuId': self.skuId,
           'properties': self.properties,
           'picUrl': self.picUrl,
           'count': self.count,
           'commentStatus': self.commentStatus,
           'price': self.price,
           'discountPrice': self.discountPrice,
           'deliveryPrice': self.deliveryPrice,
           'adjustPrice': self.adjustPrice,
           'payPrice': self.payPrice,
           'couponPrice': self.couponPrice,
           'pointPrice': self.pointPrice,
           'usePoint': self.usePoint,
           'givePoint': self.givePoint,
           'vipPrice': self.vipPrice,
           'afterSaleId': self.afterSaleId,
           'afterSaleStatus': self.afterSaleStatus,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeOrderItem.id,TradeOrderItem.userId,TradeOrderItem.orderId,TradeOrderItem.cartId,TradeOrderItem.spuId,TradeOrderItem.spuName,TradeOrderItem.skuId,TradeOrderItem.properties,TradeOrderItem.picUrl,TradeOrderItem.count,TradeOrderItem.commentStatus,TradeOrderItem.price,TradeOrderItem.discountPrice,TradeOrderItem.deliveryPrice,TradeOrderItem.adjustPrice,TradeOrderItem.payPrice,TradeOrderItem.couponPrice,TradeOrderItem.pointPrice,TradeOrderItem.usePoint,TradeOrderItem.givePoint,TradeOrderItem.vipPrice,TradeOrderItem.afterSaleId,TradeOrderItem.afterSaleStatus]