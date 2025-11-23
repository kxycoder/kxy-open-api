from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class PayChannel(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'pay_channel'


    id = Column('id',Integer, comment='商户编号',primary_key=True,autoincrement=True)
    code = Column('code',String(32), comment='渠道编码')
    status = Column('status',Integer, comment='开启状态')
    remark = Column('remark',String(255), comment='备注')
    feeRate = Column('fee_rate',String(0), comment='渠道费率，单位：百分比')
    appId = Column('app_id',Integer, comment='应用编号')
    config = Column('config',String(15000), comment='支付渠道配置')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['status', 'feeRate', 'appId']
    InsertOtherFields= ['code', 'remark', 'config']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'code': self.code,
           'status': self.status,
           'remark': self.remark,
           'feeRate': self.feeRate,
           'appId': self.appId,
           'config': self.config,
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
           'code': self.code,
           'remark': self.remark,
           'feeRate': self.feeRate,
           'appId': self.appId,
           'config': self.config,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [PayChannel.id,PayChannel.code,PayChannel.remark,PayChannel.feeRate,PayChannel.appId,PayChannel.config]