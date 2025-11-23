from abc import abstractmethod
from typing import Dict, Union, List
from app import db
from dto.site_setting_detail_dal import SiteSettingDetailDal


class MessageUtilBase(object):
    def __init__(self, dic_type):
        self.__init_config(dic_type)

    def __init_config(self, dic_type):
        """
        Args:
            app_key: 应用的 app_key
            app_secret: 应用的 app_secret
            robot_webhook: 群机器人的 webhook 地址
            robot_secret: 群机器人的加签密钥
            agent_id: 应用的 AgentId
        """
        brand_id, system_code = 1, 'CRM'
        # setting_dal = SiteSettingDetailDal(None, db.session)
        # self.confi_dict = setting_dal.GetDictSettings(brand_id, system_code, dic_type)
        self.app_key = self.confi_dict['app_key']
        self.app_secret = self.confi_dict['app_secret']
        self.robot_webhook = self.confi_dict['robot_webhook']
        self.robot_secret = self.confi_dict['robot_secret']
        self.agent_id = self.confi_dict['agent_id']

    @abstractmethod
    def sync_department(self, content):
        pass

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
