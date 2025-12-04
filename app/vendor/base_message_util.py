from abc import abstractmethod
import asyncio
from typing import Dict, Union, List, Tuple
from kxy.framework.kxy_logger import KxyLogger
from kxy.framework.http_client import HttpClient
from app.global_var import Gkey, Keys
logger = KxyLogger.getLogger(__name__)
from app.database import redisClient

qywx_access_token = None
static_app_key = None
static_app_sec = None
class MessageUtilBase(object):
    def __init__(self,app_key,app_sec) -> None:
        global static_app_key,static_app_sec
        static_app_key = app_key
        static_app_sec = app_sec
    def get_app_key(self):
        global static_app_key
        return static_app_key
    def get_app_sec(self):
        global static_app_sec
        return static_app_sec
    @abstractmethod
    def TypeName(self):
        pass
    @abstractmethod
    def sync_department(self, content):
        pass
    async def refresh_token_task(self):
        global qywx_access_token
        while True:
            try: 
                logger.debug(f'refresh_{self.TypeName}_token_task start')
                await self.refresh_access_token()
            except Exception as ex:
                logger.error(f'refresh_token_task error:{ex}')
            finally:
                await asyncio.sleep(60)

    async def refresh_access_token(self, force=0):
        global qywx_access_token
        key = Keys.QYWX_ACCESSTOKEN.value+':'+self.TypeName
        if force == 0 or force == '0':
            qywx_access_token = await redisClient.get_string(key)
            if qywx_access_token is not None:
                realKey = redisClient.gen_key(key)
                ttl = await redisClient.client.ttl(realKey)
                if ttl > 600:
                    return

        logger.info(f"refresh_{self.TypeName}_access_token")
        qywx_access_token,expires_in = await self.get_access_token()
        if qywx_access_token:
            await redisClient.set(key, qywx_access_token,expires_in)
            logger.info(f"refresh_{self.TypeName}_access_token success, expires_in:{expires_in}")
        else:
            logger.error(f"refresh_{self.TypeName}_access_token failed")
    @abstractmethod
    async def get_access_token(self)->Tuple[str,int]:
        pass
    def _get_access_token(self):
        global qywx_access_token
        return qywx_access_token
    @abstractmethod
    def send_work_text(self, user_ids: Union[str, List[str]], content: str,
                       dept_ids: Union[str, List[str]] = []) -> Dict:
        """
        发送工作通知文本消息

        Args:
            user_ids: 接收者的用户ID列表
            content: 消息内容
            dept_ids: 接收者的部门ID列表
        """
        pass

    @abstractmethod
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

    @abstractmethod
    def send_work_action_card(self, user_ids: Union[str, List[str]], title: str,
                              content: str, btns: List[Dict[str, str]], btn_orientation: str = "1",
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

    @abstractmethod
    def send_robot_text(self, content: str, at_mobiles: List[str] = [], at_all: bool = False) -> Dict:
        """
        发送群机器人文本消息

        Args:
            content: 消息内容
            at_mobiles: 需要@的手机号列表
            at_all: 是否@所有人
        """
        pass

    @abstractmethod
    def send_robot_markdown(self, title: str, content: str, at_mobiles: List[str] = None, at_all: bool = False) -> Dict:
        """
        发送群机器人markdown消息

        Args:
            title: 消息标题
            content: markdown格式的消息内容
            at_mobiles: 需要@的手机号列表
            at_all: 是否@所有人
        """
        pass

    @abstractmethod
    def send_robot_action_card(self, title: str, content: str, btns: List[Dict[str, str]], btn_orientation: str = "1",
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
    @abstractmethod
    async def list_departments(self, department_id=None):
        """
        获取部门列表

        Args:
            department_id: 部门ID，不填则获取所有部门

        Returns:
            Dict: {"errcode": int, "errmsg": str, "departments": [{"id": Any, "name": str, "parentId": Any}]}
        """
        pass
    @abstractmethod
    async def list_users(self, department_id=1, fetch_child=1):
        "获取用户列表"
        pass
