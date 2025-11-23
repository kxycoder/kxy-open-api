import base64
import hmac
import json
import time
import urllib.parse
from hashlib import sha256
from typing import Dict, Union, List
import requests
from app.common.base_message_util import MessageUtilBase

class DingDingUtil(MessageUtilBase):
    """
    钉钉消息发送类，支持群机器人消息和工作通知消息
    """

    def __init__(self):
        """
        初始化钉钉消息发送类
        """
        MessageUtilBase.__init__(self, 'dingding')
        self.url = 'https://oapi.dingtalk.com'
        self.access_token = None
        self.token_expires = 0

    def _get_access_token(self) -> str:
        """获取访问令牌"""
        if self.access_token and time.time() < self.token_expires:
            return self.access_token

        url = f"{self.url}/gettoken"
        params = {
            "app_key": self.app_key,
            "app_secret": self.app_secret
        }

        response = requests.get(url, params=params)
        result = response.json()

        if result.get("errcode") == 0:
            self.access_token = result.get("access_token")
            self.token_expires = time.time() + 7000  # Token有效期为7200秒，提前200秒刷新
            return self.access_token
        else:
            raise Exception(f"获取access_token失败: {result}")

    def _get_robot_sign(self) -> Dict[str, str]:
        """获取群机器人签名"""
        timestamp = str(round(time.time() * 1000))
        string_to_sign = f"{timestamp}\n{self.robot_secret}"
        hmac_code = hmac.new(
            self.robot_secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            digestmod=sha256
        ).digest()

        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return {
            "timestamp": timestamp,
            "sign": sign
        }

    def send_work_text(self, user_ids: Union[str, List[str]], content: str,
                       dept_ids: Union[str, List[str]] = []) -> Dict:
        """
        发送工作通知文本消息

        Args:
            user_ids: 接收者的用户ID列表
            content: 消息内容
            dept_ids: 接收者的部门ID列表
        """
        if isinstance(user_ids, str):
            user_ids = [user_ids]
        if isinstance(dept_ids, str):
            dept_ids = [dept_ids]

        url = f"{self.url}/topapi/message/corpconversation/asyncsend_v2"
        params = {
            "access_token": self._get_access_token()
        }

        data = {
            "agent_id": self.agent_id,
            "userid_list": ",".join(user_ids),
            "dept_id_list": ",".join(dept_ids) if dept_ids else [],
            "msg": {
                "msgtype": "text",
                "text": {
                    "content": content
                }
            }
        }

        response = requests.post(url, params=params, json=data)
        return response.json()

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
        if isinstance(user_ids, str):
            user_ids = [user_ids]
        if isinstance(dept_ids, str):
            dept_ids = [dept_ids]
        url = f"{self.url}/topapi/message/corpconversation/asyncsend_v2"
        params = {
            "access_token": self._get_access_token()
        }

        data = {
            "agent_id": self.agent_id,
            "userid_list": ",".join(user_ids),
            "dept_id_list": ",".join(dept_ids) if dept_ids else "",
            "msg": {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": content
                }
            }
        }

        response = requests.post(url, params=params, json=data)
        return response.json()

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
        if isinstance(user_ids, str):
            user_ids = [user_ids]

        url = f"{self.url}/topapi/message/corpconversation/asyncsend_v2"
        params = {
            "access_token": self._get_access_token()
        }

        data = {
            "agent_id": self.agent_id,
            "userid_list": ",".join(user_ids),
            "msg": {
                "msgtype": "action_card",
                "action_card": {
                    "title": title,
                    "markdown": content,
                    "btn_orientation": btn_orientation,
                    "btn_json_list": btns
                }
            }
        }

        if single_title and single_url:
            data["msg"]["action_card"].update({
                "single_title": single_title,
                "single_url": single_url
            })

        print(data)
        response = requests.post(url, params=params, json=data)
        return response.json()

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
                "content": content
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": at_all
            }
        }

        params = self._get_robot_sign() if self.robot_secret else {}
        print(params)
        response = requests.post(self.robot_webhook, params=params, json=data)
        return response.json()

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
                "title": title,
                "text": content
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": at_all
            }
        }

        params = self._get_robot_sign() if self.robot_secret else {}
        response = requests.post(self.robot_webhook, params=params, json=data)
        return response.json()

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
        data = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": content,
                "btnOrientation": btn_orientation
            }
        }

        if single_title and single_url:
            data["actionCard"].update({
                "singleTitle": single_title,
                "singleURL": single_url
            })
        else:
            data["actionCard"]["btns"] = btns

        params = self._get_robot_sign() if self.robot_secret else {}
        response = requests.post(self.robot_webhook, params=params, json=data)
        return response.json()

    def list_departments(self, department_id=None):
        access_token = self._get_access_token()
        payload = {}
        if department_id:
            payload['dept_id'] = department_id
        else:
            payload['dept_id'] = 1
        url = f"{self.url}/topapi/v2/department/listsub?access_token={access_token}"
        response = requests.post(url, data=json.dumps(payload))
        result = response.json()
        return result

    def list_users(self, department_id=None):
        access_token = self._get_access_token()
        payload = {'cursor': 0, 'size': 10}
        if department_id:
            payload['dept_id'] = department_id
        else:
            payload['dept_id'] = 1
        url = f"{self.url}/topapi/v2/user/list?access_token={access_token}"
        response = requests.post(url, data=json.dumps(payload))
        result = response.json()
        return result
