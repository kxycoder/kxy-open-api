import json
import time
from typing import Dict, Union, List

import requests

from app.common.base_message_util import MessageUtilBase
from kxy.framework.friendly_exception import FriendlyException

class WxUtil(MessageUtilBase):
    def __init__(self) -> None:
        """
        初始化钉钉消息发送类

        Args:
            app_key: 钉钉应用的 app_key
            app_secret: 钉钉应用的 app_secret
            robot_webhook: 群机器人的 webhook 地址
            robot_secret: 群机器人的加签密钥
            agent_id: 应用的 AgentId
        """
        MessageUtilBase.__init__(self, 'weixin')
        self.url = 'https://oapi.dingtalk.com'
        self.access_token = None
        self.token_expires = 0
        self.url = ''
        self.api_access_token = ''

    def _get_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(
            'ww7e14e79de2afc6e0', 'nxKfNU4-Jzg7gmI9DM2PyTSp1BZQ51QeQO8Zwl6mCso')
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        result = response.json()
        return result['access_token']

    def _get_access_token(self) -> str:
        """获取访问令牌"""
        url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_key}&secret={self.app_secret}'
        response = requests.get(url)
        result = response.json()
        return result.get('access_token')

    def send_work_text(self, user_ids: Union[str, List[str]], content: str,
                       dept_ids: Union[str, List[str]] = []) -> Dict:
        """
        发送工作通知文本消息

        Args:
            user_ids: 接收者的用户ID列表
            content: 消息内容
            dept_ids: 接收者的部门ID列表
        """
        self._send_wechat_msg(user_ids, 'text', content)

    def send_work_markdown(self, user_ids: Union[str, List[str]], title: str,
                           content: str, dept_ids: Union[str, List[str]] = None) -> Dict:
        """
        发送工作通知markdown消息

        Args:
            user_ids: 接收者的用户ID列表
            title: 消息标题
            content: markdown格式的消息内容
            dept_ids: 接收者的部门ID列表
        """
        pass

    def send_work_action_card(self, user_ids: Union[str, List[str]], title: str,
                              content: str, btns: List[Dict[str, str]],
                              btn_orientation: str = "1",
                              single_title: str = None, single_url: str = None) -> Dict:
        """
        发送工作通知卡片消息

        Args:
            user_ids: 接收者的用户ID列表
            title: 卡片标题
            content: markdown格式的卡片内容
            btns: 按钮列表，格式为[{"title": "按钮标题", "actionURL": "跳转链接"}]
            btn_orientation: 按钮排列方向，0-按钮竖直排列，1-按钮横向排列
            single_title: 整体跳转时的标题（单个按钮）
            single_url: 整体跳转时的链接（单个按钮）
        """
        pass

    def _send_wechat_msg(self, toUser, msgtype, content, first_time=True):
        token = self._get_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
        if msgtype not in ['text', 'textcard', 'markdown', 'taskcard']:
            raise FriendlyException('不支持的消息类型')
        payload = {
            "touser": '|'.join(toUser),
            "msgtype": msgtype,
            "agentid": self.agent_id,
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        if msgtype in ['text', 'textcard', 'markdown', 'taskcard']:
            payload[msgtype] = content
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        result = response.json()
        if result.get('errcode') in [40014, 42001] and first_time is True:
            self._send_wechat_msg(toUser, msgtype, content, False)
        errmsg = result.get('errmsg')
        return errmsg

    def _send_robot(self, data):
        header = {"Content-Type": "application/json"}
        resp = requests.post(self.robot_url, headers=header, data=json.dumps(data))
        return resp.json()

    def send_robot_text(self, content: str, at_mobiles: List[str] = [],
                        at_all: bool = False) -> Dict:
        """
        发送群机器人文本消息

        Args:
            content: 消息内容
            at_mobiles: 需要@的手机号列表
            at_all: 是否@所有人
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": [],
                "mentioned_mobile_list": at_mobiles
            }
        }
        res = self._send_robot(data)
        if 'errcode' in res and res['errcode'] == 45009:
            time.sleep(60)
            print(f'企微发送频率被限制，等待60s')
            return self.send_robot_text(content, at_mobiles)
        return res

    def send_robot_markdown(self, title: str, content: str,
                            at_mobiles: List[str] = None, at_all: bool = False) -> Dict:
        """
        发送群机器人markdown消息

        Args:
            title: 消息标题
            content: markdown格式的消息内容
            at_mobiles: 需要@的手机号列表
            at_all: 是否@所有人
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content,
            }
        }
        res = self._send(data)
        if 'errcode' in res and res['errcode'] == 45009:
            time.sleep(60)
            print(f'企微发送频率被限制，等待60s')
            return self.send_markdown(content)
        return res

    def send_robot_action_card(self, title: str, content: str,
                               btns: List[Dict[str, str]], btn_orientation: str = "1",
                               single_title: str = None, single_url: str = None) -> Dict:
        """
        发送群机器人卡片消息

        Args:
            title: 卡片标题
            content: markdown格式的卡片内容
            btns: 按钮列表，格式为[{"title": "按钮标题", "actionURL": "跳转链接"}]
            btn_orientation: 按钮排列方向，0-按钮竖直排列，1-按钮横向排列
            single_title: 整体跳转时的标题（单个按钮）
            single_url: 整体跳转时的链接（单个按钮）
        """
        pass

    def get_wx_user_info(self, access_token, openid):
        url = f'https://api.weixin.qq.com/cgi-bin/user/info?access_token={access_token}&openid={openid}'
        response = requests.get(url)
        result = response.json()
        return result

    def get_wx_user_openid(self, code):

        url = f'https://api.weixin.qq.com/sns/jscode2session?appid={self.app_key}&secret={self.app_secret}&js_code={code}&grant_type=authorization_code'
        response = requests.get(url)
        result = response.json()
        if str(result.get('errcode')) == '40029':
            raise FriendlyException('授权码超时')
        openId = result.get('openid')
        if not openId:
            raise FriendlyException(result.get('errmsg'))
        return result.get('openid')

    def get_wx_user_phone(self, code):
        access_token = self._get_access_token()
        url = f'https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={access_token}'
        response = requests.post(url, data=json.dumps({'code': code}))
        result = response.json()
        if result.get('errcode') == '40029':
            raise FriendlyException('请重试')
        phone_info = result.get('phone_info')
        if phone_info:
            return phone_info.get('purePhoneNumber')
        else:
            raise FriendlyException(result.get('errmsg'))

    def get_api_access_token(self):
        if self.api_access_token:
            return self.api_access_token
        corpid = 'ww9991a88a0aa82b3c'
        secret = '0l4RuFENto-x7xU7XI8ovk6fc4lKTqIyJEVPdEQpIT4'
        url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}'
        response = requests.get(url)
        result = response.json()
        self.api_access_token = result.get('access_token')
        return self.api_access_token

    def list_departments(self, department_id=None):
        access_token = self.get_api_access_token()
        payload = {}
        if department_id:
            payload['id'] = department_id
        url = f'https://qyapi.weixin.qq.com/cgi-bin/department/simplelist?access_token={access_token}'
        response = requests.post(url, data=json.dumps(payload))
        result = response.json()
        if result.get('errcode') == '40029':
            raise FriendlyException('请重试')
        return result

    def list_users(self):
        access_token = self.get_api_access_token()
        url = f'https://qyapi.weixin.qq.com/cgi-bin/user/list_id?access_token={access_token}'
        response = requests.post(url)
        result = response.json()
        if result.get('errcode') == '40029':
            raise FriendlyException('请重试')
        return result
