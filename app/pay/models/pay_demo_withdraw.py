from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayDemoWithdraw(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_demo_withdraw'


    id = Column('id',Integer, comment='提现单编号',primary_key=True,autoincrement=True)
    subject = Column('subject',String(32), comment='提现标题')
    price = Column('price',Integer, comment='提现金额，单位：分')
    userAccount = Column('user_account',String(64), comment='收款人账号')
    userName = Column('user_name',String(64), comment='收款人姓名')
    type = Column('type',Integer, comment='提现方式')
    status = Column('status',Integer, comment='提现状态')
    payTransferId = Column('pay_transfer_id',Integer, comment='转账订单编号')
    transferChannelCode = Column('transfer_channel_code',String(16), comment='转账渠道')
    transferTime = Column('transfer_time',DateTime, comment='转账支付时间')
    transferErrorMsg = Column('transfer_error_msg',String(4096), comment='转账错误提示')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['price', 'type', 'status']
    InsertOtherFields= ['subject', 'userAccount', 'userName', 'payTransferId', 'transferChannelCode', 'transferTime', 'transferErrorMsg']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'subject': self.subject,
           'price': self.price,
           'userAccount': self.userAccount,
           'userName': self.userName,
           'type': self.type,
           'status': self.status,
           'payTransferId': self.payTransferId,
           'transferChannelCode': self.transferChannelCode,
           'transferTime': self.transferTime.strftime("%Y-%m-%d %H:%M:%S") if self.transferTime else None,
           'transferErrorMsg': self.transferErrorMsg,
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
           'subject': self.subject,
           'price': self.price,
           'userAccount': self.userAccount,
           'userName': self.userName,
           'type': self.type,
           'payTransferId': self.payTransferId,
           'transferChannelCode': self.transferChannelCode,
           'transferTime': self.transferTime,
           'transferErrorMsg': self.transferErrorMsg,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayDemoWithdraw.id,PayDemoWithdraw.subject,PayDemoWithdraw.price,PayDemoWithdraw.userAccount,PayDemoWithdraw.userName,PayDemoWithdraw.type,PayDemoWithdraw.payTransferId,PayDemoWithdraw.transferChannelCode,PayDemoWithdraw.transferTime,PayDemoWithdraw.transferErrorMsg]