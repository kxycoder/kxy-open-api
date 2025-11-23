from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger,JSON

class SystemSmsChannel(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_sms_channel'

    id = Column('id',BigInteger, comment='编号',primary_key=True,autoincrement=True)
    signature = Column('signature',String(12), comment='短信签名')
    code = Column('code',String(63), comment='渠道编码')
    status = Column('status',Integer, comment='开启状态')
    remark = Column('remark',String(255), comment='备注')
    apiKey = Column('api_key',String(128), comment='短信 API 的账号')
    apiSecret = Column('api_secret',String(128), comment='短信 API 的秘钥')
    callbackUrl = Column('callback_url',String(255), comment='短信发送回调 URL')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = ['status']

    InsertOtherFields= ['signature', 'code', 'remark', 'apiKey', 'apiSecret', 'callbackUrl']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'signature': self.signature,
           'code': self.code,
           'status': self.status,
           'remark': self.remark,
           'apiKey': self.apiKey,
           'apiSecret': self.apiSecret,
           'callbackUrl': self.callbackUrl,
           'creator': self.creator,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updater': self.updater,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'deleted': self.deleted,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'signature': self.signature,
           'code': self.code,
           'remark': self.remark,
           'apiKey': self.apiKey,
           'apiSecret': self.apiSecret,
           'callbackUrl': self.callbackUrl,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemSmsChannel.id,SystemSmsChannel.signature,SystemSmsChannel.code,SystemSmsChannel.remark,SystemSmsChannel.apiKey,SystemSmsChannel.apiSecret,SystemSmsChannel.callbackUrl]