from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger,Boolean
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class TradeOrder(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'trade_order'


    id = Column('id',Integer, comment='订单编号',primary_key=True,autoincrement=True)
    no = Column('no',String(32), comment='订单流水号')
    type = Column('type',Integer, comment='订单类型')
    terminal = Column('terminal',Integer, comment='订单来源终端')
    userId = Column('user_id',Integer, comment='用户编号')
    userIp = Column('user_ip',String(30), comment='用户 IP')
    userRemark = Column('user_remark',String(200), comment='用户备注')
    status = Column('status',Integer, comment='订单状态')
    productCount = Column('product_count',Integer, comment='购买的商品数量')
    cancelType = Column('cancel_type',Integer, comment='取消类型')
    remark = Column('remark',String(200), comment='商家备注')
    commentStatus = Column('comment_status',Integer, comment='是否评价')
    brokerageUserId = Column('brokerage_user_id',Integer, comment='推广人编号')
    payOrderId = Column('pay_order_id',Integer, comment='支付订单编号')
    payStatus = Column('pay_status',Boolean, comment='是否已支付：[0:未支付 1:已经支付过]')
    payTime = Column('pay_time',DateTime, comment='订单支付时间')
    payChannelCode = Column('pay_channel_code',String(16), comment='支付成功的支付渠道')
    finishTime = Column('finish_time',DateTime, comment='订单完成时间')
    cancelTime = Column('cancel_time',DateTime, comment='订单取消时间')
    totalPrice = Column('total_price',Integer, comment='商品原价（总），单位：分')
    discountPrice = Column('discount_price',Integer, comment='订单优惠（总），单位：分')
    deliveryPrice = Column('delivery_price',Integer, comment='运费金额，单位：分')
    adjustPrice = Column('adjust_price',Integer, comment='订单调价（总），单位：分')
    payPrice = Column('pay_price',Integer, comment='应付金额（总），单位：分')
    deliveryType = Column('delivery_type',Integer, comment='配送类型')
    logisticsId = Column('logistics_id',Integer, comment='发货物流公司编号')
    logisticsNo = Column('logistics_no',String(64), comment='物流公司单号')
    deliveryTime = Column('delivery_time',DateTime, comment='发货时间')
    receiveTime = Column('receive_time',DateTime, comment='收货时间')
    receiverName = Column('receiver_name',String(20), comment='收件人名称')
    receiverMobile = Column('receiver_mobile',String(20), comment='收件人手机')
    receiverAreaId = Column('receiver_area_id',Integer, comment='收件人地区编号')
    receiverDetailAddress = Column('receiver_detail_address',String(255), comment='收件人详细地址')
    pickUpStoreId = Column('pick_up_store_id',Integer, comment='自提门店编号')
    pickUpVerifyCode = Column('pick_up_verify_code',String(64), comment='自提核销码')
    refundStatus = Column('refund_status',Integer, comment='售后状态')
    refundPrice = Column('refund_price',Integer, comment='退款金额，单位：分')
    couponId = Column('coupon_id',Integer, comment='优惠劵编号')
    couponPrice = Column('coupon_price',Integer, comment='优惠劵减免金额，单位：分')
    usePoint = Column('use_point',Integer, comment='使用的积分')
    pointPrice = Column('point_price',Integer, comment='积分抵扣的金额')
    givePoint = Column('give_point',Integer, comment='赠送的积分')
    refundPoint = Column('refund_point',Integer, comment='退还的使用的积分')
    vipPrice = Column('vip_price',Integer, comment='VIP 减免金额，单位：分')
    giveCouponTemplateCounts = Column('give_coupon_template_counts',String(255), comment='赠送的优惠劵')
    giveCouponIds = Column('give_coupon_ids',String(255), comment='赠送的优惠劵编号')
    seckillActivityId = Column('seckill_activity_id',Integer, comment='秒杀活动编号')
    bargainActivityId = Column('bargain_activity_id',Integer, comment='砍价活动编号')
    bargainRecordId = Column('bargain_record_id',Integer, comment='砍价记录编号')
    combinationActivityId = Column('combination_activity_id',Integer, comment='拼团活动编号')
    combinationHeadId = Column('combination_head_id',Integer, comment='拼团团长编号')
    combinationRecordId = Column('combination_record_id',Integer, comment='拼团记录编号')
    pointActivityId = Column('point_activity_id',Integer, comment='积分活动编号')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')
    items=[]
    user={}
    logs=[]

    InsertRequireFields = ['type', 'terminal', 'status', 'productCount', 'commentStatus', 'payStatus', 'totalPrice', 'discountPrice', 'deliveryPrice', 'adjustPrice', 'payPrice', 'deliveryType', 'refundStatus', 'refundPrice', 'couponPrice', 'usePoint', 'pointPrice', 'givePoint', 'refundPoint', 'vipPrice']
    InsertOtherFields= ['no', 'userId', 'userIp', 'userRemark', 'cancelType', 'remark', 'brokerageUserId', 'payOrderId', 'payTime', 'payChannelCode', 'finishTime', 'cancelTime', 'logisticsId', 'logisticsNo', 'deliveryTime', 'receiveTime', 'receiverName', 'receiverMobile', 'receiverAreaId', 'receiverDetailAddress', 'pickUpStoreId', 'pickUpVerifyCode', 'couponId', 'giveCouponTemplateCounts', 'giveCouponIds', 'seckillActivityId', 'bargainActivityId', 'bargainRecordId', 'combinationActivityId', 'combinationHeadId', 'combinationRecordId', 'pointActivityId']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'no': self.no,
           'type': self.type,
           'terminal': self.terminal,
           'userId': self.userId,
           'userIp': self.userIp,
           'userRemark': self.userRemark,
           'status': self.status,
           'productCount': self.productCount,
           'cancelType': self.cancelType,
           'remark': self.remark,
           'commentStatus': self.commentStatus,
           'brokerageUserId': self.brokerageUserId,
           'payOrderId': self.payOrderId,
           'payStatus': self.payStatus,
           'payTime': self.payTime.strftime("%Y-%m-%d %H:%M:%S") if self.payTime else None,
           'payChannelCode': self.payChannelCode,
           'finishTime': self.finishTime.strftime("%Y-%m-%d %H:%M:%S") if self.finishTime else None,
           'cancelTime': self.cancelTime.strftime("%Y-%m-%d %H:%M:%S") if self.cancelTime else None,
           'totalPrice': self.totalPrice,
           'discountPrice': self.discountPrice,
           'deliveryPrice': self.deliveryPrice,
           'adjustPrice': self.adjustPrice,
           'payPrice': self.payPrice,
           'deliveryType': self.deliveryType,
           'logisticsId': self.logisticsId,
           'logisticsNo': self.logisticsNo,
           'deliveryTime': self.deliveryTime.strftime("%Y-%m-%d %H:%M:%S") if self.deliveryTime else None,
           'receiveTime': self.receiveTime.strftime("%Y-%m-%d %H:%M:%S") if self.receiveTime else None,
           'receiverName': self.receiverName,
           'receiverMobile': self.receiverMobile,
           'receiverAreaId': self.receiverAreaId,
           'receiverDetailAddress': self.receiverDetailAddress,
           'pickUpStoreId': self.pickUpStoreId,
           'pickUpVerifyCode': self.pickUpVerifyCode,
           'refundStatus': self.refundStatus,
           'refundPrice': self.refundPrice,
           'couponId': self.couponId,
           'couponPrice': self.couponPrice,
           'usePoint': self.usePoint,
           'pointPrice': self.pointPrice,
           'givePoint': self.givePoint,
           'refundPoint': self.refundPoint,
           'vipPrice': self.vipPrice,
           'giveCouponTemplateCounts': self.giveCouponTemplateCounts,
           'giveCouponIds': self.giveCouponIds,
           'seckillActivityId': self.seckillActivityId,
           'bargainActivityId': self.bargainActivityId,
           'bargainRecordId': self.bargainRecordId,
           'combinationActivityId': self.combinationActivityId,
           'combinationHeadId': self.combinationHeadId,
           'combinationRecordId': self.combinationRecordId,
           'pointActivityId': self.pointActivityId,
           'creator': self.creator,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updater': self.updater,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'deleted': self.deleted,
           'tenantId': self.tenantId,
           'items': [item.to_basic_dict() for item in self.items] if self.items else [],

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'no': self.no,
           'type': self.type,
           'terminal': self.terminal,
           'userId': self.userId,
           'userIp': self.userIp,
           'userRemark': self.userRemark,
           'productCount': self.productCount,
           'cancelType': self.cancelType,
           'remark': self.remark,
           'commentStatus': self.commentStatus,
           'brokerageUserId': self.brokerageUserId,
           'payOrderId': self.payOrderId,
           'payStatus': self.payStatus,
           'payTime': self.payTime,
           'payChannelCode': self.payChannelCode,
           'finishTime': self.finishTime,
           'cancelTime': self.cancelTime,
           'totalPrice': self.totalPrice,
           'discountPrice': self.discountPrice,
           'deliveryPrice': self.deliveryPrice,
           'adjustPrice': self.adjustPrice,
           'payPrice': self.payPrice,
           'deliveryType': self.deliveryType,
           'logisticsId': self.logisticsId,
           'logisticsNo': self.logisticsNo,
           'deliveryTime': self.deliveryTime,
           'receiveTime': self.receiveTime,
           'receiverName': self.receiverName,
           'receiverMobile': self.receiverMobile,
           'receiverAreaId': self.receiverAreaId,
           'receiverDetailAddress': self.receiverDetailAddress,
           'pickUpStoreId': self.pickUpStoreId,
           'pickUpVerifyCode': self.pickUpVerifyCode,
           'refundStatus': self.refundStatus,
           'refundPrice': self.refundPrice,
           'couponId': self.couponId,
           'couponPrice': self.couponPrice,
           'usePoint': self.usePoint,
           'pointPrice': self.pointPrice,
           'givePoint': self.givePoint,
           'refundPoint': self.refundPoint,
           'vipPrice': self.vipPrice,
           'giveCouponTemplateCounts': self.giveCouponTemplateCounts,
           'giveCouponIds': self.giveCouponIds,
           'seckillActivityId': self.seckillActivityId,
           'bargainActivityId': self.bargainActivityId,
           'bargainRecordId': self.bargainRecordId,
           'combinationActivityId': self.combinationActivityId,
           'combinationHeadId': self.combinationHeadId,
           'combinationRecordId': self.combinationRecordId,
           'pointActivityId': self.pointActivityId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeOrder.id,TradeOrder.no,TradeOrder.type,TradeOrder.terminal,TradeOrder.userId,TradeOrder.userIp,TradeOrder.userRemark,TradeOrder.productCount,TradeOrder.cancelType,TradeOrder.remark,TradeOrder.commentStatus,TradeOrder.brokerageUserId,TradeOrder.payOrderId,TradeOrder.payStatus,TradeOrder.payTime,TradeOrder.payChannelCode,TradeOrder.finishTime,TradeOrder.cancelTime,TradeOrder.totalPrice,TradeOrder.discountPrice,TradeOrder.deliveryPrice,TradeOrder.adjustPrice,TradeOrder.payPrice,TradeOrder.deliveryType,TradeOrder.logisticsId,TradeOrder.logisticsNo,TradeOrder.deliveryTime,TradeOrder.receiveTime,TradeOrder.receiverName,TradeOrder.receiverMobile,TradeOrder.receiverAreaId,TradeOrder.receiverDetailAddress,TradeOrder.pickUpStoreId,TradeOrder.pickUpVerifyCode,TradeOrder.refundStatus,TradeOrder.refundPrice,TradeOrder.couponId,TradeOrder.couponPrice,TradeOrder.usePoint,TradeOrder.pointPrice,TradeOrder.givePoint,TradeOrder.refundPoint,TradeOrder.vipPrice,TradeOrder.giveCouponTemplateCounts,TradeOrder.giveCouponIds,TradeOrder.seckillActivityId,TradeOrder.bargainActivityId,TradeOrder.bargainRecordId,TradeOrder.combinationActivityId,TradeOrder.combinationHeadId,TradeOrder.combinationRecordId,TradeOrder.pointActivityId]