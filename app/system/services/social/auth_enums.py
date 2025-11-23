from enum import Enum
from abc import ABC, abstractmethod

class AuthResponseStatus:
    UNSUPPORTED = "UNSUPPORTED"

class AuthException(Exception):
    def __init__(self, status):
        self.status = status




class AuthSource(ABC):
    @abstractmethod
    def authorize(self):
        pass
    
    @abstractmethod
    def access_token(self):
        pass
    
    @abstractmethod
    def user_info(self):
        pass

class AuthTypes(Enum):
    DINGTALK = 20
    GITEE = 10
    DINGTALK_V2 = 20
    WECHAT_MINI_PROGRAM = 34
    WECHAT_OPEN = 32
    WECHAT_GONZHONGHAO = 31
    WECHAT = 30
    # 建立 AuthTypes 与处理类的映射关系
    _AUTH_TYPE_MAP = {
        # 注意：这里需要将映射关系放在类方法之外定义，避免循环引用
    }
    
    @classmethod
    def _init_auth_type_map(cls):
        """初始化认证类型映射表"""
        
        cls._AUTH_TYPE_MAP = {
            cls.DINGTALK: DingTalkAuth,
            cls.GITEE: GiteeAuth,
            cls.DINGTALK_V2: DingTalkV2Auth,
            cls.WECHAT_MINI_PROGRAM: WechatMiniProgramAuth,
            # 添加其他类型的映射
        }
    
    @classmethod
    def get_auth_handler(cls, auth_type)->'AuthSource':
        """
        根据 AuthTypes 获取对应的处理类实例
        
        Args:
            auth_type: AuthTypes 枚举值
            
        Returns:
            对应的 AuthSource 实例
            
        Raises:
            ValueError: 当不支持的 auth_type 传入时
        """
        # 延迟初始化映射表，避免导入时循环引用
        if not hasattr(cls, '_AUTH_TYPE_MAP') or not cls._AUTH_TYPE_MAP:
            cls._init_auth_type_map()
            
        handler_class = cls._AUTH_TYPE_MAP.get(auth_type)
        if not handler_class:
            raise ValueError(f"Unsupported auth type: {auth_type}")
        
        return handler_class()

class DingTalkAuth(AuthSource):
    def authorize(self) :
        return "https://oapi.dingtalk.com/connect/qrconnect"
    
    def access_token(self):
        raise AuthException(AuthResponseStatus.UNSUPPORTED)
    
    def  user_info(self):
        return "https://oapi.dingtalk.com/sns/getuserinfo_bycode"

class GiteeAuth(AuthSource):
    def authorize(self):
        return "https://gitee.com/oauth/authorize"

    def access_token(self):
        return "https://gitee.com/oauth/token"

    def user_info(self):
        return "https://gitee.com/api/v5/user"

    
class DingTalkV2Auth(AuthSource):
    def authorize(self):
        return "https://login.dingtalk.com/oauth2/challenge.htm"

    def access_token(self):
        return "https://api.dingtalk.com/v1.0/oauth2/userAccessToken"

    def user_info(self):
        return "https://api.dingtalk.com/v1.0/contact/users/me"

    
class WechatMiniProgramAuth(AuthSource):
    def authorize(self):
        raise AuthException("不支持获取授权 url，请使用小程序内置函数 wx.login() 登录获取 code")

    def access_token(self):
        return "https://api.weixin.qq.com/sns/jscode2session"

    def user_info(self):
        raise AuthException("不支持获取用户信息 url，请使用小程序内置函数 wx.getUserProfile() 获取用户信息")

class WeChatQiyeWeixinAuth(AuthSource):
    def authorize(self):
        return "https://open.work.weixin.qq.com/wwopen/sso/qrConnect"

    def access_token(self):
        return "https://qyapi.weixin.qq.com/cgi-bin/gettoken"

    def user_info(self):
        return "https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo"
    
class CodingAuth(AuthSource):
    def authorize(self):
        return "https://%s.coding.net/oauth_authorize.html"

    def access_token(self):
        return "https://%s.coding.net/api/oauth/access_token"

    def user_info(self):
        return "https://%s.coding.net/api/account/current_user"
