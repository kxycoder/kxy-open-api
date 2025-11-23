from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class TradeBrokerageWithdraw(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'trade_brokerage_withdraw'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    userId = Column('user_id',Integer, comment='用户编号')
    price = Column('price',Integer, comment='提现金额')
    feePrice = Column('fee_price',Integer, comment='提现手续费')
    totalPrice = Column('total_price',Integer, comment='当前总佣金')
    type = Column('type',Integer, comment='提现类型')
    userName = Column('user_name',String(64), comment='真实姓名')
    userAccount = Column('user_account',String(64), comment='账号')
    bankName = Column('bank_name',String(100), comment='银行名称')
    bankAddress = Column('bank_address',String(200), comment='开户地址')
    qrCodeUrl = Column('qr_code_url',String(512), comment='收款码')
    status = Column('status',Integer, comment='状态：0-审核中，10-审核通过 20-审核不通过；11 - 提现成功；21-提现失败')
    auditReason = Column('audit_reason',String(128), comment='审核驳回原因')
    auditTime = Column('audit_time',DateTime, comment='审核时间')
    remark = Column('remark',String(500), comment='备注')
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


    InsertRequireFields = ['userId', 'price', 'feePrice', 'totalPrice', 'type', 'status']
    InsertOtherFields= ['userName', 'userAccount', 'bankName', 'bankAddress', 'qrCodeUrl', 'auditReason', 'auditTime', 'remark', 'payTransferId', 'transferChannelCode', 'transferTime', 'transferErrorMsg']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'price': self.price,
           'feePrice': self.feePrice,
           'totalPrice': self.totalPrice,
           'type': self.type,
           'userName': self.userName,
           'userAccount': self.userAccount,
           'bankName': self.bankName,
           'bankAddress': self.bankAddress,
           'qrCodeUrl': self.qrCodeUrl,
           'status': self.status,
           'auditReason': self.auditReason,
           'auditTime': self.auditTime.strftime("%Y-%m-%d %H:%M:%S") if self.auditTime else None,
           'remark': self.remark,
           'payTransferId': self.payTransferId,
           'transferChannelCode': self.transferChannelCode,
           'transferTime': self.transferTime.strftime("%Y-%m-%d %H:%M:%S") if self.transferTime else None,
           'transferErrorMsg': self.transferErrorMsg,
           'creator': self.creator,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updater': self.updater,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'deleted': self.deleted,
           'tenantId': self.tenantId
        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'userId': self.userId,
           'price': self.price,
           'feePrice': self.feePrice,
           'totalPrice': self.totalPrice,
           'type': self.type,
           'userName': self.userName,
           'userAccount': self.userAccount,
           'bankName': self.bankName,
           'bankAddress': self.bankAddress,
           'qrCodeUrl': self.qrCodeUrl,
           'auditReason': self.auditReason,
           'auditTime': self.auditTime,
           'remark': self.remark,
           'payTransferId': self.payTransferId,
           'transferChannelCode': self.transferChannelCode,
           'transferTime': self.transferTime,
           'transferErrorMsg': self.transferErrorMsg,
        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeBrokerageWithdraw.id,TradeBrokerageWithdraw.userId,TradeBrokerageWithdraw.price,TradeBrokerageWithdraw.feePrice,TradeBrokerageWithdraw.totalPrice,TradeBrokerageWithdraw.type,TradeBrokerageWithdraw.userName,TradeBrokerageWithdraw.userAccount,TradeBrokerageWithdraw.bankName,TradeBrokerageWithdraw.bankAddress,TradeBrokerageWithdraw.qrCodeUrl,TradeBrokerageWithdraw.auditReason,TradeBrokerageWithdraw.auditTime,TradeBrokerageWithdraw.remark,TradeBrokerageWithdraw.payTransferId,TradeBrokerageWithdraw.transferChannelCode,TradeBrokerageWithdraw.transferTime,TradeBrokerageWithdraw.transferErrorMsg]