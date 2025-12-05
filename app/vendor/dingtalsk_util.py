import asyncio
import json
import time
from typing import Dict, Union, List
import requests
from app.contract.types.department_vo import DepartmentVO
from app.vendor.base_message_util import MessageUtilBase
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.kxy_logger import KxyLogger
from kxy.framework.http_client import HttpClient
logger = KxyLogger.getLogger(__name__)

class DingTalkUtil(MessageUtilBase):
    TypeName='dingtalk'
    def __init__(self, appkey, appsecret):
        self.appkey = appkey
        self.appsecret = appsecret
        self.platform = 'dingtalk'  # 添加平台标识
        self._access_token = None
        self._token_expire_time = 0

    async def get_access_token(self):
        url = f"{self.url}/gettoken?appkey={self.get_app_key()}&appsecret={self.get_app_sec()}"
        response = await HttpClient.get(url)
        result = response.json()
        return result.get('access_token'),result.get('expires_in')
    
    def sync_department(self, content):
        """
        同步部门信息
        """
        pass

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
            "userid_list": ",".join(user_ids) if user_ids else "",
            "dept_id_list": ",".join(dept_ids) if dept_ids else "",
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
            "userid_list": ",".join(user_ids) if user_ids else "",
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

        if single_title and single_url:
            # 整体跳转动作卡片
            data = {
                "agent_id": self.agent_id,
                "userid_list": ",".join(user_ids) if user_ids else "",
                "msg": {
                    "msgtype": "action_card",
                    "action_card": {
                        "title": title,
                        "markdown": content,
                        "single_title": single_title,
                        "single_url": single_url
                    }
                }
            }
        elif btns:
            # 独立跳转动作卡片
            btn_json_list = []
            for btn in btns:
                btn_json_list.append({
                    "title": btn["title"],
                    "action_url": btn["actionURL"]
                })

            data = {
                "agent_id": self.agent_id,
                "userid_list": ",".join(user_ids) if user_ids else "",
                "msg": {
                    "msgtype": "action_card",
                    "action_card": {
                        "title": title,
                        "markdown": content,
                        "btn_orientation": btn_orientation,
                        "btn_json_list": btn_json_list
                    }
                }
            }
        else:
            raise ValueError("Either single_title/single_url or btns must be provided")

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
        if not self.robot_webhook:
            raise FriendlyException("未配置机器人webhook地址")

        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }

        if at_all:
            data["text"]["at"] = {"isAtAll": True}
        elif at_mobiles:
            data["text"]["at"] = {"atMobiles": at_mobiles}

        headers = {"Content-Type": "application/json"}
        response = requests.post(self.robot_webhook, headers=headers, data=json.dumps(data))
        result = response.json()

        if 'errcode' in result and result['errcode'] == 45009:
            time.sleep(60)
            print(f'钉钉发送频率被限制，等待60s')
            return self.send_robot_text(content, at_mobiles, at_all)

        return result

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
        if not self.robot_webhook:
            raise FriendlyException("未配置机器人webhook地址")

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": content
            }
        }

        # 钉钉的@功能需要在content中以@手机号的方式体现
        if at_all:
            data["markdown"]["text"] += "\n\n@all"
        elif at_mobiles:
            for mobile in at_mobiles:
                data["markdown"]["text"] += f"\n\n@{mobile}"

        headers = {"Content-Type": "application/json"}
        response = requests.post(self.robot_webhook, headers=headers, data=json.dumps(data))
        result = response.json()

        if 'errcode' in result and result['errcode'] == 45009:
            time.sleep(60)
            print(f'钉钉发送频率被限制，等待60s')
            return self.send_robot_markdown(title, content, at_mobiles, at_all)

        return result

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
        if not self.robot_webhook:
            raise FriendlyException("未配置机器人webhook地址")

        if single_title and single_url:
            # 整体跳转动作卡片
            data = {
                "actionCard": {
                    "title": title,
                    "text": content,
                    "singleTitle": single_title,
                    "singleURL": single_url
                },
                "msgtype": "actionCard"
            }
        elif btns:
            # 独立跳转动作卡片
            btns_list = [{"title": btn["title"], "actionURL": btn["actionURL"]} for btn in btns]
            data = {
                "actionCard": {
                    "title": title,
                    "text": content,
                    "btnOrientation": btn_orientation,
                    "btns": btns_list
                },
                "msgtype": "actionCard"
            }
        else:
            raise ValueError("Either single_title/single_url or btns must be provided")

        headers = {"Content-Type": "application/json"}
        response = requests.post(self.robot_webhook, headers=headers, data=json.dumps(data))
        return response.json()
    def convert_to_standard_department(self, source_dept: dict) -> DepartmentVO:
        """
        将不同来源的部门数据转换为标准的DepartmentVO对象
        
        Args:
            source_dept: 来源于不同系统的部门原始数据
            
        Returns:
            DepartmentVO: 标准化的部门对象
        """
        # 根据不同平台做字段映射
        
        # 钉钉平台字段映射
        dept_id = source_dept.get('dept_id')
        dept_name = source_dept.get('name')
        parent_id = source_dept.get('parent_id', 0)
        
        # 创建标准部门VO对象
        department_vo = DepartmentVO(
            id=dept_id,
            name=dept_name,
            parent_id=parent_id,
            level=source_dept.get('level') or source_dept.get('order'),
            principal_user_id=source_dept.get('principal_userid'),
            principal_user_name=source_dept.get('principal_username'),
            child_ids=source_dept.get('child_ids'),
            dep_type=source_dept.get('dep_type') or source_dept.get('type'),
            sort=source_dept.get('sort') or source_dept.get('order'),
            status=0,  # 默认启用
            creator="system",
            updater="system",
        )
        
        return department_vo
    async def list_departments(self, department_id=None):
        """
        获取部门列表

        Args:
            department_id: 部门ID，不填则获取根部门下的子部门（通常ID为1）
        """
        access_token = self._get_access_token()
        # 如果没有指定部门ID，则默认获取根部门(1)的子部门
        if department_id is None:
            department_id = 1
            
        url = f"{self.url}/topapi/v2/department/listsub?access_token={access_token}"
        data = {
            "dept_id": department_id
        }
        response = await HttpClient.post(url, json=data)
        result = response.json()
        if result.get('errcode') != 0:
            raise FriendlyException(result.get('errmsg'))

        dept_list = result.get('result', {}).get('dept_list', [])
        normalized_departments = []
        for dept in dept_list:
            normalized_dept = self.convert_to_standard_department(dept)
            normalized_departments.append(normalized_dept)

        return normalized_departments

    async def list_users(self, department_id=1, fetch_child=1):
        """
        获取用户列表

        Args:
            department_id: 部门ID
            fetch_child: 是否递归获取子部门用户
            
        Returns:
            返回用户ID列表
        """
        access_token = self._get_access_token()
        url = f"{self.url}/topapi/user/list"
        params = {
            "access_token": access_token
        }
        data = {
            "dept_id": department_id,
            "cursor": 0,
            "size": 100,
            "order_field": "modify_desc",
            "fetch_child": fetch_child
        }
        
        all_user_ids = []
        while True:
            response = await HttpClient.post(url, params=params, json=data)
            result = response.json()
            
            if result.get("errcode") != 0:
                raise Exception(f"获取用户列表失败: {result.get('errmsg')}")
                
            user_list = result.get("result", {}).get("data", [])
            if not user_list:
                break
                
            all_user_ids.extend(user_list)
            
            # 检查是否还有更多数据
            has_more = result.get("result", {}).get("has_more", False)
            if not has_more:
                break
                
            # 更新游标继续获取下一页
            data["cursor"] = result.get("result", {}).get("next_cursor", 0)
            
        return {"errcode": 0, "errmsg": "ok", "userlist": all_user_ids}

    def get_user_info(self, userid):
        """
        根据用户ID获取用户信息
        """
        access_token = self._get_access_token()
        url = f"{self.url}/topapi/v2/user/get?access_token={access_token}"
        data = {
            "userid": userid
        }
        response = requests.post(url, json=data)
        return response.json()

    def get_user_by_code(self, code):
        """
        通过临时授权码获取用户信息
        """
        access_token = self._get_access_token()
        url = f"{self.url}/topapi/v2/user/getuserinfo?access_token={access_token}"
        data = {
            "code": code
        }
        response = requests.post(url, json=data)
        result = response.json()
        if result.get('errcode') == 40029:
            raise FriendlyException('授权码超时')
        if result.get('errcode') != 0:
            raise FriendlyException(result.get('errmsg'))
        return result
