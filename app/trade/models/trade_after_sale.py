from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant
from kxy.framework.base_entity import JSONString

@FilterTenant()
class TradeAfterSale(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'trade_after_sale'


    id = Column('id',Integer, comment='售后编号',primary_key=True,autoincrement=True)
    no = Column('no',String(32), comment='售后单号')
    type = Column('type',Integer, comment='售后类型')
    status = Column('status',Integer, comment='售后状态')
    way = Column('way',Integer, comment='售后方式')
    userId = Column('user_id',Integer, comment='用户编号')
    applyReason = Column('apply_reason',String(255), comment='申请原因')
    applyDescription = Column('apply_description',String(255), comment='补充描述')
    applyPicUrls = Column('apply_pic_urls',String(255), comment='补充凭证图片')
    orderId = Column('order_id',Integer, comment='订单编号')
    orderNo = Column('order_no',String(32), comment='订单流水号')
    orderItemId = Column('order_item_Id',Integer, comment='订单项编号')
    spuId = Column('spu_id',Integer, comment='商品 SPU 编号')
    spuName = Column('spu_name',String(255), comment='商品 SPU 名称')
    skuId = Column('sku_id',Integer, comment='商品 SKU 编号')
    properties = Column('properties',JSONString(2000), comment='商品属性数组，JSON 格式')
    picUrl = Column('pic_url',String(200), comment='商品图片')
    count = Column('count',Integer, comment='购买数量')
    auditTime = Column('audit_time',DateTime, comment='审批时间')
    auditUserId = Column('audit_user_id',Integer, comment='审批人')
    auditReason = Column('audit_reason',String(255), comment='审批备注')
    refundPrice = Column('refund_price',Integer, comment='退款金额，单位：分')
    payRefundId = Column('pay_refund_id',Integer, comment='支付退款编号')
    refundTime = Column('refund_time',DateTime, comment='退款时间')
    logisticsId = Column('logistics_id',Integer, comment='退货物流公司编号')
    logisticsNo = Column('logistics_no',String(64), comment='退货物流单号')
    deliveryTime = Column('delivery_time',DateTime, comment='退货时间')
    receiveTime = Column('receive_time',DateTime, comment='收货时间')
    receiveReason = Column('receive_reason',String(255), comment='收货备注')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')
    order={}
    orderItem={}
    user={}
    logs=[]

    InsertRequireFields = ['status', 'way', 'count', 'refundPrice']
    InsertOtherFields= ['no', 'type', 'userId', 'applyReason', 'applyDescription', 'applyPicUrls', 'orderId', 'orderNo', 'orderItemId', 'spuId', 'spuName', 'skuId', 'properties', 'picUrl', 'auditTime', 'auditUserId', 'auditReason', 'payRefundId', 'refundTime', 'logisticsId', 'logisticsNo', 'deliveryTime', 'receiveTime', 'receiveReason']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'no': self.no,
           'type': self.type,
           'status': self.status,
           'way': self.way,
           'userId': self.userId,
           'applyReason': self.applyReason,
           'applyDescription': self.applyDescription,
           'applyPicUrls': self.applyPicUrls,
           'orderId': self.orderId,
           'orderNo': self.orderNo,
           'orderItemId': self.orderItemId,
           'spuId': self.spuId,
           'spuName': self.spuName,
           'skuId': self.skuId,
           'properties': self.properties,
           'picUrl': self.picUrl,
           'count': self.count,
           'auditTime': self.auditTime.strftime("%Y-%m-%d %H:%M:%S") if self.auditTime else None,
           'auditUserId': self.auditUserId,
           'auditReason': self.auditReason,
           'refundPrice': self.refundPrice,
           'payRefundId': self.payRefundId,
           'refundTime': self.refundTime.strftime("%Y-%m-%d %H:%M:%S") if self.refundTime else None,
           'logisticsId': self.logisticsId,
           'logisticsNo': self.logisticsNo,
           'deliveryTime': self.deliveryTime.strftime("%Y-%m-%d %H:%M:%S") if self.deliveryTime else None,
           'receiveTime': self.receiveTime.strftime("%Y-%m-%d %H:%M:%S") if self.receiveTime else None,
           'receiveReason': self.receiveReason,
           'creator': self.creator,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updater': self.updater,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'deleted': self.deleted,
           'tenantId': self.tenantId,
           'order': self.order.to_basic_dict() if self.order and hasattr(self.order, 'to_basic_dict') else self.order,
           'orderItem': self.orderItem.to_basic_dict() if self.orderItem and hasattr(self.orderItem, 'to_basic_dict') else self.orderItem,
           'user': self.user.to_basic_dict() if self.user and hasattr(self.user, 'to_basic_dict') else self.user,
           'logs': [log.to_basic_dict() for log in self.logs] if self.logs and isinstance(self.logs, list) else [],

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'no': self.no,
           'type': self.type,
           'way': self.way,
           'userId': self.userId,
           'applyReason': self.applyReason,
           'applyDescription': self.applyDescription,
           'applyPicUrls': self.applyPicUrls,
           'orderId': self.orderId,
           'orderNo': self.orderNo,
           'orderItemId': self.orderItemId,
           'spuId': self.spuId,
           'spuName': self.spuName,
           'skuId': self.skuId,
           'properties': self.properties,
           'picUrl': self.picUrl,
           'count': self.count,
           'auditTime': self.auditTime,
           'auditUserId': self.auditUserId,
           'auditReason': self.auditReason,
           'refundPrice': self.refundPrice,
           'payRefundId': self.payRefundId,
           'refundTime': self.refundTime,
           'logisticsId': self.logisticsId,
           'logisticsNo': self.logisticsNo,
           'deliveryTime': self.deliveryTime,
           'receiveTime': self.receiveTime,
           'receiveReason': self.receiveReason,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeAfterSale.id,TradeAfterSale.no,TradeAfterSale.type,TradeAfterSale.way,TradeAfterSale.userId,TradeAfterSale.applyReason,TradeAfterSale.applyDescription,TradeAfterSale.applyPicUrls,TradeAfterSale.orderId,TradeAfterSale.orderNo,TradeAfterSale.orderItemId,TradeAfterSale.spuId,TradeAfterSale.spuName,TradeAfterSale.skuId,TradeAfterSale.properties,TradeAfterSale.picUrl,TradeAfterSale.count,TradeAfterSale.auditTime,TradeAfterSale.auditUserId,TradeAfterSale.auditReason,TradeAfterSale.refundPrice,TradeAfterSale.payRefundId,TradeAfterSale.refundTime,TradeAfterSale.logisticsId,TradeAfterSale.logisticsNo,TradeAfterSale.deliveryTime,TradeAfterSale.receiveTime,TradeAfterSale.receiveReason]