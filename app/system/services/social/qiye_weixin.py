from app.system.api.types.vo_request import VoSocialUser
from app.system.services.social.auth_token import AuthToken
from .auth_enums import WeChatQiyeWeixinAuth
import json
import requests
from kxy.framework.date_util import DateUtil
from app.system.models.system_social_client import SystemSocialClient
from kxy.framework.http_client import HttpClient
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)
class QiyeWeixin():
    def __init__(self,source:WeChatQiyeWeixinAuth,config:SystemSocialClient):
        self.source = source
        self.config:SystemSocialClient = config
        self.access_token = ''
    def get_auth_url(self,state,):
        return f"{self.source.authorize()}?agentid={self.config.agentId}&appid={self.config.clientId}&lang=zh&state={state}&redirect_uri={self.config.redirectUri}"
    
    async def get_user_info(self, auth_token:AuthToken):
        """
        获取用户信息
        :param auth_token: 认证token
        :return: 用户信息
        """
        # access token loginurl = $"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}";
        # url = "https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=#{access_token}#&code=" + code;
        code = auth_token.code

        url =await self.user_info_url(auth_token)
        logger.info(url)
        # 发送POST请求获取用户信息
        response =await HttpClient.get(
            url,
            headers={'Content-Type': 'application/json'}
        )
        
        result = response.json()
        
        # 检查是否有错误
        if result.get("errcode", 0) != 0:
            raise Exception(result.get("errmsg", "获取用户信息失败"))
        print(result)
        UserId = result.get("UserId")
        if not UserId:
            raise Exception("不支持的平台")
        access_token = await self.get_access_token()
        userDeltailUrl = f'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={access_token}&userid={UserId}'
        detailResponse = await HttpClient.get(userDeltailUrl)
        user_info = detailResponse.json()
        if user_info.get("errcode", 0) != 0:
            raise Exception(user_info.get("errmsg", "获取用户信息失败"))
            
        # 构造返回的token对象
        token = {}
        
        # 构造并返回用户对象
        result= {
            "rawUserInfo": {},
            "unionid": UserId,
            "nickname": user_info.get("alias"),
            "username": user_info.get("name"),
            "avatar": user_info.get("avatar"),
            "gender": "UNKNOWN",  # 假设AuthUserGender.UNKNOWN对应"UNKNOWN"
            "source": str(self.source),
            "rawToken": token,
            "token": code,
        }
        return VoSocialUser(**result)

    async def get_access_token(self):
        """
        获取企业微信应用access_token
        """
        if self.access_token:
            return self.access_token
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.config.clientId}&corpsecret={self.config.clientSecret}"
        response = await HttpClient.get(url)
        result = response.json()
        
        if result.get("errcode") == 0:
            self.access_token = result.get("access_token")
            return self.access_token
        else:
            raise Exception(f"获取access_token失败: {result.get('errmsg')}")

    async def user_info_url(self, auth_token:AuthToken):
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
        access_token =await self.get_access_token()
        return f"{self.source.user_info()}?access_token={access_token}&code={auth_token.access_code}"