from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger, Time
from kxy.framework.filter_tenant import FilterTenant
from kxy.framework.base_entity import JSONString

@FilterTenant()
class TradeDeliveryPickUpStore(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        self.verifyUsers = None  # 核销用户详细信息（非数据库字段）

    __tablename__ = 'trade_delivery_pick_up_store'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    name = Column('name',String(64), comment='门店名称')
    introduction = Column('introduction',String(256), comment='门店简介')
    phone = Column('phone',String(16), comment='门店手机')
    areaId = Column('area_id',Integer, comment='区域编号')
    detailAddress = Column('detail_address',String(256), comment='门店详细地址')
    logo = Column('logo',String(256), comment='门店 logo')
    openingTime = Column('opening_time',Time, comment='营业开始时间')
    closingTime = Column('closing_time',Time, comment='营业结束时间')
    latitude = Column('latitude',String(0), comment='纬度')
    longitude = Column('longitude',String(0), comment='经度')
    verifyUserIds = Column('verify_user_ids',JSONString(256), comment='核销用户编号数组')
    status = Column('status',Integer, comment='门店状态')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')
    verifyUsers=[]

    InsertRequireFields = ['areaId', 'openingTime', 'closingTime', 'latitude', 'longitude', 'status']
    InsertOtherFields= ['name', 'introduction', 'phone', 'detailAddress', 'logo', 'verifyUserIds']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'introduction': self.introduction,
           'phone': self.phone,
           'areaId': self.areaId,
           'detailAddress': self.detailAddress,
           'logo': self.logo,
           'openingTime': self.openingTime,
           'closingTime': self.closingTime,
           'latitude': self.latitude,
           'longitude': self.longitude,
           'verifyUserIds': self.verifyUserIds,
           'verifyUsers': self.verifyUsers if hasattr(self, 'verifyUsers') else None,
           'status': self.status,
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
           'name': self.name,
           'introduction': self.introduction,
           'phone': self.phone,
           'areaId': self.areaId,
           'detailAddress': self.detailAddress,
           'logo': self.logo,
           'openingTime': self.openingTime,
           'closingTime': self.closingTime,
           'latitude': self.latitude,
           'longitude': self.longitude,
           'verifyUserIds': self.verifyUserIds,
           'verifyUsers': self.verifyUsers if hasattr(self, 'verifyUsers') else None,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [TradeDeliveryPickUpStore.id,TradeDeliveryPickUpStore.name,TradeDeliveryPickUpStore.introduction,TradeDeliveryPickUpStore.phone,TradeDeliveryPickUpStore.areaId,TradeDeliveryPickUpStore.detailAddress,TradeDeliveryPickUpStore.logo,TradeDeliveryPickUpStore.openingTime,TradeDeliveryPickUpStore.closingTime,TradeDeliveryPickUpStore.latitude,TradeDeliveryPickUpStore.longitude,TradeDeliveryPickUpStore.verifyUserIds]