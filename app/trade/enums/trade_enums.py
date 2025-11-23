from enum import IntEnum


class OrderStatusEnum(IntEnum):
    """订单状态枚举"""
    UNPAID = 0  # 待付款
    UNDELIVERED = 10  # 待发货
    DELIVERED = 20  # 已发货
    COMPLETED = 30  # 已完成
    CANCELED = 40  # 已取消

    @classmethod
    def get_desc(cls, status):
        """获取状态描述"""
        desc_map = {
            cls.UNPAID: '待付款',
            cls.UNDELIVERED: '待发货',
            cls.DELIVERED: '已发货',
            cls.COMPLETED: '已完成',
            cls.CANCELED: '已取消'
        }
        return desc_map.get(status, '未知状态')


class OrderOperateTypeEnum(IntEnum):
    """订单操作类型枚举"""
    CREATE = 10  # 创建订单
    PAY = 20  # 支付订单
    DELIVERY = 30  # 发货
    RECEIVE = 40  # 收货
    COMMENT = 50  # 评价
    CANCEL = 60  # 取消订单
    REFUND = 70  # 退款

    @classmethod
    def get_desc(cls, operate_type):
        """获取操作类型描述"""
        desc_map = {
            cls.CREATE: '创建订单',
            cls.PAY: '支付订单',
            cls.DELIVERY: '发货',
            cls.RECEIVE: '收货',
            cls.COMMENT: '评价',
            cls.CANCEL: '取消订单',
            cls.REFUND: '退款'
        }
        return desc_map.get(operate_type, '未知操作')


class UserTypeEnum(IntEnum):
    """用户类型枚举"""
    MEMBER = 1  # 会员用户
    ADMIN = 2  # 管理员

    @classmethod
    def get_desc(cls, user_type):
        """获取用户类型描述"""
        desc_map = {
            cls.MEMBER: '会员用户',
            cls.ADMIN: '管理员'
        }
        return desc_map.get(user_type, '未知类型')
