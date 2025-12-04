from app.system.api.types.vo_request import VoSocialUser
from app.system.services.social.auth_token import AuthToken
from app.system.services.social.base_auth import BaseAuth
from .auth_enums import EzrLoginAuth
from app.system.models.system_social_client import SystemSocialClient
from kxy.framework.http_client import HttpClient
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)
class EZRSSO(BaseAuth):
    def __init__(self,source:EzrLoginAuth,config:SystemSocialClient):
        super().__init__(source,config)
    def get_auth_url(self,state,):
        return f"{self.source.authorize()}?returnUrl={self.config.redirectUri}"
    
    async def get_user_info(self, auth_token:AuthToken):
        """
        获取用户信息
        :param auth_token: 认证token
        :return: 用户信息
        """
        code = auth_token.token

        url =await self.user_info_url(auth_token)
        logger.info(url)
        # 发送POST请求获取用户信息
        response =await HttpClient.get(
            url,
            headers={'Content-Type': 'application/json'}
        )
        
        result = response.json()
        
        # 检查是否有错误
        if result.get("status_code", 0) != 200:
            raise Exception(result.get("errmsg", "获取用户信息失败"))
        # {'data': {'id': 43, 'username': 'liujiguo', 'phone': '18601650373', 'chineseName': '刘吉国'}, 'status': True, 'status_code': 200, 'errors': None}

        user_info = result.get("data")
        UserId = user_info.get("id")
        if not UserId:
            raise Exception("不支持的平台")
        detailResult = await HttpClient.get(f'https://log-ops.ezrpro.cn/api/User?id={UserId}&token={auth_token.token}')
        detailInfo = detailResult.json().get('data')
        
        # 构造并返回用户对象
        result= {
            "rawUserInfo": detailInfo,
            "unionid": str(UserId),
            "nickname": user_info.get("chineseName"),
            "username": user_info.get("username"),
            "phone": user_info.get("phone"),
            "gender": "UNKNOWN",  # 假设AuthUserGender.UNKNOWN对应"UNKNOWN"
            "source": str(self.source),
            "rawToken": {"code": auth_token.token},
            "department": str(detailInfo.get('department')),
            "avatar": detailInfo.get('avatar'),
            "qyId": detailInfo.get('userID'),
            "email": detailInfo.get('email'),
            "token": code,
        }
        return VoSocialUser(**result,tenantId=self.config.tenantId)

    async def get_access_token(self):
        """
        获取企业微信应用access_token
        """
        return 

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
        return f"{self.source.user_info()}?token={auth_token.token}"