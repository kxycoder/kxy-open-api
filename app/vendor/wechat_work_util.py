import asyncio
import json
import time
from typing import Dict, Union, List

import requests

from app.contract.types.department_vo import DepartmentVO, UserVO
from app.vendor.base_message_util import MessageUtilBase
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.http_client import HttpClient
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

class WeChatWorkUtil(MessageUtilBase):
    TypeName='wechat_work'
    def __init__(self,app_key,app_sec) -> None:
        """
        初始化企业微信消息发送类
        """
        super().__init__(app_key,app_sec)
        self.platform = 'wechat_work'  # 添加平台标识
        self.url = 'https://qyapi.weixin.qq.com'

    async def get_access_token(self):
        url = f"{self.url}/cgi-bin/gettoken?corpid={self.get_app_key()}&corpsecret={self.get_app_sec()}"
        response = await HttpClient.get(url)
        result = response.json()
        return result.get('access_token'),result.get('expires_in')

    def send_work_text(self, user_ids: Union[str, List[str]], content: str,
                       dept_ids: Union[str, List[str]] = []) -> Dict:
        """
        发送工作通知文本消息

        Args:
            user_ids: 接收者的用户ID列表
            content: 消息内容
            dept_ids: 接收者的部门ID列表
        """
        return self._send_wechat_msg(user_ids, 'text', {'content': content})

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
        # 企业微信不使用标题参数，所以忽略title
        return self._send_wechat_msg(user_ids, 'markdown', {'content': content})

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
        # 企业微信没有专门的卡片消息类型，这里使用markdown模拟
        card_content = f"### {title}\n\n{content}"
        if btns:
            for btn in btns:
                card_content += f"\n\n[{btn['title']}]({btn['actionURL']})"

        return self._send_wechat_msg(user_ids, 'markdown', {'content': card_content})

    def _send_wechat_msg(self, toUser, msgtype, content, first_time=True):
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self._get_access_token()}"
        
        if isinstance(toUser, str):
            toUser = [toUser]
            
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
            
        return result

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
                "mentioned_list": ["@all"] if at_all else [],
                "mentioned_mobile_list": at_mobiles
            }
        }
        return self._send_robot(data)

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
        return self._send_robot(data)

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
        # 企业微信群机器人没有原生的卡片消息类型，使用markdown格式模拟
        card_content = f"### {title}\n\n{content}"
        if btns:
            for btn in btns:
                card_content += f"\n\n[{btn['title']}]({btn['actionURL']})"
                
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": card_content,
            }
        }
        return self._send_robot(data)

    def _send_robot(self, data):
        if not self.robot_webhook:
            raise FriendlyException("未配置机器人webhook地址")
            
        header = {"Content-Type": "application/json"}
        resp = requests.post(self.robot_webhook, headers=header, data=json.dumps(data))
        return resp.json()

    def get_wx_user_info(self, openid):
        url = f'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={self._get_access_token()}&userid={openid}'
        response = requests.get(url)
        result = response.json()
        return result

    def get_wx_user_openid(self, code):
        url = f'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token={self._get_access_token()()}&code={code}'
        response = requests.get(url)
        result = response.json()
        if result.get('errcode') == 40029:
            raise FriendlyException('授权码超时')
        user_id = result.get('UserId')
        if not user_id:
            raise FriendlyException(result.get('errmsg'))
        return user_id

    def get_wx_user_phone(self, code):
        url = f'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token={self._get_access_token()}&code={code}'
        response = requests.get(url)
        result = response.json()
        if result.get('errcode') == 40029:
            raise FriendlyException('请重试')
        # 企业微信不能直接获取手机号，只能获取用户ID，需要额外调用接口获取手机号
        user_id = result.get('UserId')
        if user_id:
            return user_id
        else:
            raise FriendlyException(result.get('errmsg'))
    def convert_to_standard_department(self, source_dept: dict) -> DepartmentVO:
        """
        将不同来源的部门数据转换为标准的DepartmentVO对象
        
        Args:
            source_dept: 来源于不同系统的部门原始数据
            
        Returns:
            DepartmentVO: 标准化的部门对象
        """
        
        dept_id = source_dept.get('id')
        dept_name = source_dept.get('name')
        parent_id = source_dept.get('parentid', 0)
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
            tenant_id=self.tenantId or 1
        )
        
        return department_vo
    async def list_departments(self, department_id=None)->List[DepartmentVO]:
        url = f'https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token={self._get_access_token()}'
        if department_id:
            url += f"&id={department_id}"
        response = await HttpClient.get(url)
        result = response.json()
        if result.get('errcode') != 0:
            return result

        normalized_departments = []
        for dept in result.get('department', []):
            department_vo = await self.convert_to_standard_department(dept)
            normalized_departments.append(department_vo)

        return normalized_departments

    async def list_users(self, department_id=1, fetch_child=1):
        url = f'https://qyapi.weixin.qq.com/cgi-bin/user/list?access_token={self._get_access_token()}&department_id={department_id}&fetch_child={fetch_child}'
        response = await HttpClient.get(url)
        result = response.json()
        if result.get('errcode') != 0:
            raise FriendlyException('请重试')
        
        users = []
        for user_data in result.get('userlist', []):
            user_vo = UserVO(
                user_id=user_data.get('userid', ''),
                username=user_data.get('userid', ''),
                nickname=user_data.get('name', ''),
                mobile=user_data.get('mobile'),
                email=user_data.get('email'),
                department_id=user_data.get('department', [None])[0] if user_data.get('department') else None,
                position=user_data.get('position'),
                is_leader=bool(user_data.get('isleader', 0)),
                avatar=user_data.get('avatar'),
                gender=user_data.get('gender'),
                status=0 if user_data.get('status') == 1 else 1,  # 微信企业号中1表示已激活(在职)，0表示禁用(离职)
                remark=user_data.get('alias'),  # 使用别名作为备注
                creator="system",
                updater="system"
            )
            users.append(user_vo)
            
        return users
