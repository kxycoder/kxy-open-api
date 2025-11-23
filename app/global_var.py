from enum import Enum
from app.config import config
from kxy.framework.context import current_tenant_id
class Keys(Enum):
    # todo 将所有的redis的key，其他的Key放在这里管理
    WX_ACCESSTOKEN=config.SystemCode+":WX:ACCESSTOKEN"
    """KXY:WX:ACCESSTOKEN"""
    USER_API_TOKEN = config.SystemCode+":token:{}"
    """KXY:token:{USERID}"""
    USER_PERMISSION=config.SystemCode+':permission:{}:{}:{}:{}'
    '''用户权限permission:{SystemCode}:{user_id}:{moduleName}:{resource}'''
    USER_SCHEMAS=config.SystemCode+':permission:{}:{}:{}'
    """KXY:permission:{tenant}:{user_id}:{resource}"""
    USER_ROLES = config.SystemCode+":Roles:{}:{}"
    '''KXY:RoleIds:{tenantId}:{USERID}'''
    USER_ROLES_ID = config.SystemCode+":RolesId:{}:{}"
    '''KXY:RoleIds:{tenantId}:{USERID}'''
    PUBLIC_DICTIONARY_CACHE_KEY= "{}:dictionary:{}"
    """字典：{systemcode}:dictionary:{dictype}"""
    PUBLIC_DICTIONARY_CACHE_TYPE_KEY="""{}:dictionary:{}:{}"""
    """字典：{systemcode}:dictionary:{dictype}:{int}"""
    USER_TENANT_KEY="KXY:tenant:{}"
    """KXY:tenant:{USERID}"""

    
class Gkey(str):
    """生成Key，管理Key"""
    def __new__(cls,key:Keys,*args):
        v=key.value.format(*args)
        return v

# 发送类型(1-微信 2-邮件 3-短信)
class SendTypes(Enum):
    """发送类型"""
    Wechat = 1
    '''微信'''
    Email = 2
    '''邮件'''
    Sms = 3
    '''短信'''
# 发送状态(1-创建 3-待发送 4-发送中 9-失败 10-删除)
class SendStatus(Enum):
    """发送状态"""
    Create = 0
    '''创建'''
    NoSend = 30
    '''不发送'''
    Success = 10
    '''发送成功'''
    Fail = 20
    '''失败'''
class ReciveStatus(Enum):
    """接收状态"""
    Waite = 0
    '''等待结果'''
    Success = 1
    '''接收成功'''
    Fail = 2
    '''失败'''

# 1: 公告; 2: 活动 3:提醒
class MsgTypes(Enum):
    """消息类型"""
    Notice = 1
    '''公告'''
    Activity = 2
    '''活动'''
    Remind = 3
    '''提醒'''
class SmsTempalteTypes(Enum):
    """短信模板类型"""
    Verify = 1
    '''验证码'''
    Notice = 2
    '''通知'''
    Marketing = 3
    '''营销'''
