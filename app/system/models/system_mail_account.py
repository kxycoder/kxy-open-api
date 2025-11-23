from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger

class SystemMailAccount(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_mail_account'

    id = Column('id',BigInteger, comment='主键',primary_key=True,autoincrement=True)
    mail = Column('mail',String(255), comment='邮箱')
    username = Column('username',String(255), comment='用户名')
    password = Column('password',String(255), comment='密码')
    host = Column('host',String(255), comment='SMTP 服务器域名')
    port = Column('port',Integer, comment='SMTP 服务器端口')
    sslEnable = Column('ssl_enable',String(1), comment='是否开启 SSL')
    starttlsEnable = Column('starttls_enable',String(1), comment='是否开启 STARTTLS')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = []

    InsertOtherFields= ['mail', 'username', 'password', 'host','port', 'sslEnable', 'starttlsEnable']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'mail': self.mail,
           'username': self.username,
           'password': self.password,
           'host': self.host,
           'port': self.port,
           'sslEnable': self.sslEnable,
           'starttlsEnable': self.starttlsEnable,
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
           'mail': self.mail,
           'username': self.username,
           'password': self.password,
           'host': self.host,
           'port': self.port,
           'sslEnable': self.sslEnable,
           'starttlsEnable': self.starttlsEnable,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemMailAccount.id,SystemMailAccount.mail,SystemMailAccount.username,SystemMailAccount.password,SystemMailAccount.host,SystemMailAccount.port,SystemMailAccount.sslEnable,SystemMailAccount.starttlsEnable]