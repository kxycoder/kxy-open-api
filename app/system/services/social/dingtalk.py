from app.system.api.types.vo_request import VoSocialAuthRedirect, VoSocialUser
from app.system.services.social.base_auth import BaseAuth
from .auth_enums import DingTalkV2Auth
import json
import requests
from kxy.framework.date_util import DateUtil
from app.system.models.system_social_client import SystemSocialClient
from kxy.framework.http_client import HttpClient

class DingTalk(BaseAuth):
    def __init__(self,source:DingTalkV2Auth,config:SystemSocialClient):
        super().__init__(source,config)
    def get_auth_url(self,state,):
        return f"{self.source.authorize()}?response_type=code&appid={self.config.clientId}&scope=snsapi_login&state={state}&redirect_uri={self.config.redirectUri}"
    
    async def get_user_info(self, auth_token:VoSocialAuthRedirect):
        """
        获取用户信息
        :param auth_token: 认证token
        :return: 用户信息
        """

        code = auth_token.code
        param = {"tmp_auth_code": code}
        url =await self.user_info_url(auth_token)
        # 发送POST请求获取用户信息
        response =await HttpClient.post(
            url,
            json=param,
            headers={'Content-Type': 'application/json'}
        )
        
        result = response.json()
        
        # 检查是否有错误
        if result.get("errcode", 0) != 0:
            raise Exception(result.get("errmsg", "获取用户信息失败"))
        
        user_info = result.get("user_info", {})
        
        # 构造返回的token对象
        token = {
            "openId": user_info.get("openid"),
            "unionId": user_info.get("unionid")
        }
        
        # 构造并返回用户对象
        result= {
            "rawUserInfo": user_info,
            "unionid": user_info.get("unionid"),
            "nickname": user_info.get("nick"),
            "username": user_info.get("nick"),
            "gender": "UNKNOWN",  # 假设AuthUserGender.UNKNOWN对应"UNKNOWN"
            "source": str(self.source),
            "rawToken": token,
            "token": code,
            "code": code,
        }
        return VoSocialUser(**result,tenantId=self.config.tenantId)
    @staticmethod
    def generate_dingtalk_signature(secret_key, timestamp):
        """
        生成钉钉签名
        :param secret_key: 密钥
        :param timestamp: 时间戳
        :return: URL编码后的签名字符串
        """
        import hmac
        import base64
        from urllib.parse import quote

        # 使用HMAC-SHA256生成签名
        signature = hmac.new(
            secret_key.encode('utf-8'),
            timestamp.encode('utf-8'),
            'sha256'
        ).digest()

        # Base64编码并解码为字符串
        base64_sign = base64.b64encode(signature).decode('utf-8')

        # URL编码处理
        return quote(base64_sign, safe='')

    async def user_info_url(self, auth_token:VoSocialAuthRedirect):
        """
        获取用户信息URL
        :param auth_token: 认证token
        :return: 用户信息URL
        """
        '''
        public static String generateDingTalkSignature(String secretKey, String timestamp) {
            byte[] signData = sign(secretKey.getBytes('utf-8'), timestamp.getBytes('utf-8'), HMAC_SHA_256);
            return urlEncode(new String(Base64Utils.encode(signData, false)));
        }
        '''
        timestamp = str(int(DateUtil.now_timestamp())*1000)
        signature = self.generate_dingtalk_signature(self.config.clientSecret, timestamp)
        return f"{self.source.user_info()}?signature={signature}&timestamp={timestamp}&accessKey={self.config.clientId}"