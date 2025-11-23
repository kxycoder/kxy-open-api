import asyncio
import json
import os
from kxy.framework.friendly_exception import FriendlyException
from app.config import config
from app.database import get_redis_client
from app.global_var import Gkey, Keys
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)
from app.tools.http_client_helper import HttpxClientHelper
class WxUtil():
    def __init__(self):
        self.base_url = "https://api.weixin.qq.com"
        self.myredis = get_redis_client()
    def genUrl(self, path):
        return f"{self.base_url}{path}"
    async def set_accesstoken(self,accesstoken):
        logger.info(f"set_accesstoken:{accesstoken}")
        key =Gkey(Keys.WX_ACCESSTOKEN)
        await self.myredis.setex(key, 7200, accesstoken)
    async def set_test_token(self,prd_token):
        if os.environ.get("FLASK_ENV")!="production":
            return
        if not config.WXTOKEN_ASYNC_URL:
            return
        url = f"{config.WXTOKEN_ASYNC_URL}?token={prd_token}"

        payload={}
        headers = {
            'token': '',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Authorization': 'Bearer '
        }
        response = await HttpxClientHelper.get(url, headers=headers, data=payload)
        print(response.text)
    async def get_once_token(self):
        url=self.genUrl(f"/cgi-bin/token?grant_type=client_credential&appid={config.wx_appid}&secret={config.wx_secret}")
        response = await HttpxClientHelper.get(url)
        result = response.json()
        return result
    
    async def get_qrcode(self,trial='1'):
        url = self.genUrl(f"/wxa/getwxacodeunlimit?access_token={self.get_accesstoken()}")
        playload = {
            "scene": "scene",
            "page": "pages/index/index",
            "check_path": False,
            "is_hyaline": True,
            "width": 200
        }
        if trial=='1':
            playload['env_version'] = 'trial'
        result=await HttpxClientHelper.post(url,json=playload,timeout=10)
        return result.content
    async def get_wx_accesstoken(self):
        key =Gkey(Keys.WX_ACCESSTOKEN)
        accesstoken =await self.myredis.get(key)
        if accesstoken is not None:
            return accesstoken.decode('utf-8')
        return ""
    async def get_user_token(self,email):
        key = Gkey(Keys.USER_API_TOKEN,email)
        token =await self.myredis.get(key)
        if token is not None:
            return token.decode('utf-8')
        return ""
    async def refresh_token_task(self):
        while True:
            try:
                logger.debug(f'refresh_wx_token_task start')
                await self.refresh_accesstoken()
            except Exception as ex:
                return logger.error(f'refresh_token_task error:{ex}')
            finally:
                await asyncio.sleep(60)
    async def refresh_accesstoken(self, force=0):
        key =Gkey(Keys.WX_ACCESSTOKEN)
        if force==0 or force=='0':
            accesstoken =await self.myredis.get(key)
            if accesstoken is not None:
                ttl =await self.myredis.ttl(key)
                if ttl > 600:
                    await self.set_test_token(accesstoken.decode('utf-8'))
                    return
        logger.info("refresh_accesstoken")
        url=self.genUrl(f"/cgi-bin/stable_token?grant_type=client_credential&appid={config.wx_appid}&secret={config.wx_secret}")
        playload={
            "grant_type":"client_credential",
            "appid":config.wx_appid,
            "secret":config.wx_secret,
            "force_refresh":False
        }
        response = await HttpxClientHelper.post(url,json=playload,timeout=10)
        result = response.json()
        print(result)
        accesstoken = result.get('access_token')
        if accesstoken:
            expires_in = result.get('expires_in', 7200)
            await self.myredis.setex(key, expires_in, accesstoken)
            await self.set_test_token(accesstoken)
            logger.info(f"refresh_accesstoken success, expires_in:{expires_in}")
            return
        logger.error(f"refresh_accesstoken failed, result:{result}")
        
    async def get_wx_user_openid(self, code):
        url =self.genUrl(f'/sns/jscode2session?appid={config.wx_appid}&secret={config.wx_secret}&js_code={code}&grant_type=authorization_code')
        response =await HttpxClientHelper.get(url)
        result = response.json()
        if str(result.get('errcode')) == '40029':
            raise FriendlyException('授权码超时')
        openId = result.get('openid')
        if not openId:
            raise FriendlyException(result.get('errmsg'))
        return result.get('openid')

    async def get_wx_user_phone(self, code):
        access_token =await self.get_wx_accesstoken()
        url = self.genUrl( f'/wxa/business/getuserphonenumber?access_token={access_token}')
        response =await HttpxClientHelper.post(url, json = {'code': code})
        result = response.json()
        if result.get('errcode') == '40029':
            raise FriendlyException('请重试')
        phone_info = result.get('phone_info')
        if phone_info:
            return phone_info.get('purePhoneNumber')
        else:
            raise FriendlyException(result.get('errmsg'))