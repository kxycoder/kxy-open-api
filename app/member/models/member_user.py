from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger,Integer
from kxy.framework.filter_tenant import FilterTenant

@FilterTenant()
class MemberUser(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'member_user'


    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    mobile = Column('mobile',String(11), comment='手机号')
    password = Column('password',String(100), comment='密码')
    status = Column('status',Integer, comment='状态')
    registerIp = Column('register_ip',String(32), comment='注册 IP')
    registerTerminal = Column('register_terminal',Integer, comment='注册终端')
    loginIp = Column('login_ip',String(50), comment='最后登录IP')
    loginDate = Column('login_date',DateTime, comment='最后登录时间')
    nickname = Column('nickname',String(30), comment='用户昵称')
    avatar = Column('avatar',String(512), comment='头像')
    name = Column('name',String(30), comment='真实名字')
    sex = Column('sex',Integer, comment='用户性别')
    areaId = Column('area_id',Integer, comment='所在地')
    birthday = Column('birthday',DateTime, comment='出生日期')
    mark = Column('mark',String(255), comment='会员备注')
    point = Column('point',Integer, comment='积分')
    tagIds = Column('tag_ids',String(255), comment='用户标签编号列表，以逗号分隔')
    levelId = Column('level_id',Integer, comment='等级编号')
    experience = Column('experience',Integer, comment='经验')
    groupId = Column('group_id',Integer, comment='用户分组编号')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')


    InsertRequireFields = ['status', 'point', 'experience']
    InsertOtherFields= ['mobile', 'password', 'registerIp', 'registerTerminal', 'loginIp', 'loginDate', 'nickname', 'avatar', 'name', 'sex', 'areaId', 'birthday', 'mark', 'tagIds', 'levelId', 'groupId']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'mobile': self.mobile,
           'password': self.password,
           'status': self.status,
           'registerIp': self.registerIp,
           'registerTerminal': self.registerTerminal,
           'loginIp': self.loginIp,
           'loginDate': self.loginDate.strftime("%Y-%m-%d %H:%M:%S") if self.loginDate else None,
           'nickname': self.nickname,
           'avatar': self.avatar,
           'name': self.name,
           'sex': self.sex,
           'areaId': self.areaId,
           'birthday': self.birthday.strftime("%Y-%m-%d %H:%M:%S") if self.birthday else None,
           'mark': self.mark,
           'point': self.point,
           'tagIds': self.tagIds,
           'levelId': self.levelId,
           'experience': self.experience,
           'groupId': self.groupId,
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
           'mobile': self.mobile,
           'password': self.password,
           'registerIp': self.registerIp,
           'registerTerminal': self.registerTerminal,
           'loginIp': self.loginIp,
           'loginDate': self.loginDate,
           'nickname': self.nickname,
           'avatar': self.avatar,
           'name': self.name,
           'sex': self.sex,
           'areaId': self.areaId,
           'birthday': self.birthday,
           'mark': self.mark,
           'point': self.point,
           'tagIds': self.tagIds,
           'levelId': self.levelId,
           'experience': self.experience,
           'groupId': self.groupId,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [MemberUser.id,MemberUser.mobile,MemberUser.password,MemberUser.status,MemberUser.registerIp,MemberUser.registerTerminal,MemberUser.loginIp,MemberUser.loginDate,MemberUser.nickname,MemberUser.avatar,MemberUser.name,MemberUser.sex,MemberUser.areaId,MemberUser.birthday,MemberUser.mark,MemberUser.point,MemberUser.tagIds,MemberUser.levelId,MemberUser.experience,MemberUser.groupId]