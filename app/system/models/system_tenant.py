from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, Integer

class SystemTenant(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_tenant'

    id = Column('id',Integer, comment='租户编号',primary_key=True,autoincrement=True)
    name = Column('name',String(30), comment='租户名')
    contactUserId = Column('contact_user_id',Integer, comment='联系人的用户编号')
    contactName = Column('contact_name',String(30), comment='联系人')
    contactMobile = Column('contact_mobile',String(500), comment='联系手机')
    status = Column('status',Integer, comment='租户状态（0正常 1停用）')
    website = Column('website',String(256), comment='绑定域名')
    packageId = Column('package_id',Integer, comment='租户套餐编号')
    expireTime = Column('expire_time',DateTime, comment='过期时间')
    accountCount = Column('account_count',Integer, comment='账号数量')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除')


    InsertRequireFields = ['status', 'packageId', 'expireTime', 'accountCount']

    InsertOtherFields= ['name', 'contactUserId', 'contactName', 'contactMobile', 'website']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'contactUserId': self.contactUserId,
           'contactName': self.contactName,
           'contactMobile': self.contactMobile,
           'status': self.status,
           'website': self.website,
           'packageId': self.packageId,
           'expireTime': self.expireTime.strftime("%Y-%m-%d %H:%M:%S") if self.expireTime else None,
           'accountCount': self.accountCount,
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
           'name': self.name,
           'contactUserId': self.contactUserId,
           'contactName': self.contactName,
           'contactMobile': self.contactMobile,
           'website': self.website,
           'packageId': self.packageId,
           'expireTime': self.expireTime,
           'accountCount': self.accountCount,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemTenant.id,SystemTenant.name,SystemTenant.contactUserId,SystemTenant.contactName,SystemTenant.contactMobile,SystemTenant.website,SystemTenant.packageId,SystemTenant.expireTime,SystemTenant.accountCount]