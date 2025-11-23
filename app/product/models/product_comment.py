from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger,Boolean
from kxy.framework.filter_tenant import FilterTenant
from kxy.framework.base_entity import JSONString

@FilterTenant()
class ProductComment(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'product_comment'

    id = Column('id',Integer, comment='评论编号，主键自增',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='评价人的用户编号，关联 MemberUserDO 的 id 编号')
    userNickname = Column('user_nickname',String(255), comment='评价人名称')
    userAvatar = Column('user_avatar',String(1024), comment='评价人头像')
    anonymous = Column('anonymous',Boolean, comment='是否匿名')
    orderId = Column('order_id',Integer, comment='交易订单编号，关联 TradeOrderDO 的 id 编号')
    orderItemId = Column('order_item_id',Integer, comment='交易订单项编号，关联 TradeOrderItemDO 的 id 编号')
    spuId = Column('spu_id',Integer, comment='商品 SPU 编号，关联 ProductSpuDO 的 id')
    spuName = Column('spu_name',String(255), comment='商品 SPU 名称')
    skuId = Column('sku_id',Integer, comment='商品 SKU 编号，关联 ProductSkuDO 的 id 编号')
    skuPicUrl = Column('sku_pic_url',String(256), comment='图片地址')
    skuProperties = Column('sku_properties',String(512), comment='属性数组，JSON 格式 [{propertId: , valueId: }, {propertId: , valueId: }]')
    visible = Column('visible',Boolean, comment='是否可见，true:显示false:隐藏')
    scores = Column('scores',Integer, comment='评分星级1-5分')
    descriptionScores = Column('description_scores',Integer, comment='描述星级 1-5 星')
    benefitScores = Column('benefit_scores',Integer, comment='服务星级 1-5 星')
    content = Column('content',String(1024), comment='评论内容')
    picUrls = Column('pic_urls',JSONString(4096), comment='评论图片地址数组')
    replyStatus = Column('reply_status',Integer, comment='商家是否回复')
    replyUserId = Column('reply_user_id',Integer, comment='回复管理员编号，关联 AdminUserDO 的 id 编号')
    replyContent = Column('reply_content',String(1024), comment='商家回复内容')
    replyTime = Column('reply_time',DateTime, comment='商家回复时间')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')
    skuProperties = []
    
    InsertRequireFields = []
    InsertOtherFields= ['userId', 'anonymous', 'spuId', 'skuId', 'scores', 'descriptionScores', 'benefitScores','userNickname', 'userAvatar', 'orderId', 'orderItemId', 'spuName', 'skuPicUrl', 'skuProperties', 'visible', 'content', 'picUrls', 'replyStatus', 'replyUserId', 'replyContent', 'replyTime']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'userNickname': self.userNickname,
           'userAvatar': self.userAvatar,
           'anonymous': self.anonymous,
           'orderId': self.orderId,
           'orderItemId': self.orderItemId,
           'spuId': self.spuId,
           'spuName': self.spuName,
           'skuId': self.skuId,
           'skuPicUrl': self.skuPicUrl,
           'skuProperties': self.skuProperties,
           'visible': self.visible,
           'scores': self.scores,
           'descriptionScores': self.descriptionScores,
           'benefitScores': self.benefitScores,
           'content': self.content,
           'picUrls': self.picUrls,
           'replyStatus': self.replyStatus,
           'replyUserId': self.replyUserId,
           'replyContent': self.replyContent,
           'replyTime': self.replyTime.strftime("%Y-%m-%d %H:%M:%S") if self.replyTime else None,
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
           'userNickname': self.userNickname,
           'userAvatar': self.userAvatar,
           'anonymous': self.anonymous,
           'orderId': self.orderId,
           'orderItemId': self.orderItemId,
           'spuId': self.spuId,
           'spuName': self.spuName,
           'skuId': self.skuId,
           'skuPicUrl': self.skuPicUrl,
           'skuProperties': self.skuProperties,
           'visible': self.visible,
           'scores': self.scores,
           'descriptionScores': self.descriptionScores,
           'benefitScores': self.benefitScores,
           'content': self.content,
           'picUrls': self.picUrls,
           'replyStatus': self.replyStatus,
           'replyUserId': self.replyUserId,
           'replyContent': self.replyContent,
           'replyTime': self.replyTime,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [ProductComment.id,ProductComment.userId,ProductComment.userNickname,ProductComment.userAvatar,ProductComment.anonymous,ProductComment.orderId,ProductComment.orderItemId,ProductComment.spuId,ProductComment.spuName,ProductComment.skuId,ProductComment.skuPicUrl,ProductComment.skuProperties,ProductComment.visible,ProductComment.scores,ProductComment.descriptionScores,ProductComment.benefitScores,ProductComment.content,ProductComment.picUrls,ProductComment.replyStatus,ProductComment.replyUserId,ProductComment.replyContent,ProductComment.replyTime]