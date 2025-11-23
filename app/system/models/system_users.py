from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter import FilterTenant
from kxy.framework.base_entity import JSONString

@FilterTenant('tenantId')
class SystemUsers(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_users'

    id = Column('id',Integer, comment='用户ID',primary_key=True,autoincrement=True)
    username = Column('username',String(30), comment='用户账号')
    password = Column('password',String(100), comment='密码')
    nickname = Column('nickname',String(30), comment='用户昵称')
    remark = Column('remark',String(500), comment='备注')
    deptId = Column('dept_id',Integer, comment='部门ID')
    postIds = Column('post_ids',JSONString(255), comment='岗位编号数组')
    email = Column('email',String(50), comment='用户邮箱')
    mobile = Column('mobile',String(11), comment='手机号码')
    sex = Column('sex',Integer, comment='用户性别')
    status = Column('status',Integer, comment='帐号状态（0正常 1停用）')
    avatar = Column('avatar',String(512), comment='头像地址')
    loginIp = Column('login_ip',String(50), comment='最后登录IP')
    loginDate = Column('login_date',DateTime, comment='最后登录时间')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = []

    InsertOtherFields= ['username', 'password', 'nickname', 'remark', 'deptId', 'postIds', 'email', 'mobile', 'sex', 'avatar', 'loginIp', 'loginDate','status', 'tenantId']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'username': self.username,
           'nickname': self.nickname,
           'remark': self.remark,
           'deptId': self.deptId,
           'postIds': self.postIds,
           'email': self.email,
           'mobile': self.mobile,
           'sex': self.sex,
           'avatar': self.avatar,
           'status': self.status,
           'loginIp': self.loginIp,
           'loginDate': self.loginDate.strftime("%Y-%m-%d %H:%M:%S") if self.loginDate else None,
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
           'username': self.username,
           'nickname': self.nickname,
           'remark': self.remark,
           'deptId': self.deptId,
           'postIds': self.postIds,
           'email': self.email,
           'mobile': self.mobile,
           'sex': self.sex,
           'avatar': self.avatar,
           'loginIp': self.loginIp,
           'loginDate': self.loginDate,
           'tenantId': self.tenantId,
        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemUsers.id,SystemUsers.username,SystemUsers.status,SystemUsers.nickname,SystemUsers.remark,SystemUsers.deptId,SystemUsers.postIds,SystemUsers.email,SystemUsers.mobile,SystemUsers.sex,SystemUsers.avatar,SystemUsers.loginIp,SystemUsers.loginDate,SystemUsers.tenantId]