from pydantic import BaseModel
from typing import Optional

class AuthToken(BaseModel):
    # 基础属性
    access_token: Optional[str] = None
    expire_in: int = 0
    refresh_token: Optional[str] = None
    refresh_token_expire_in: int = 0
    uid: Optional[str] = None
    open_id: Optional[str] = None
    access_code: Optional[str] = None
    union_id: Optional[str] = None

    # Google附带属性
    scope: Optional[str] = None
    token_type: Optional[str] = None
    id_token: Optional[str] = None

    # 小米附带属性
    mac_algorithm: Optional[str] = None
    mac_key: Optional[str] = None

    # 企业微信附带属性 (since 1.10.0)
    code: Optional[str] = None
    # 微信公众号 - 网页授权的登录时可用
    # 快照页获取的uid/oid和头像昵称是虚拟信息
    snapshot_user: bool = False

    # Twitter附带属性 (since 1.13.0)
    oauth_token: Optional[str] = None
    oauth_token_secret: Optional[str] = None
    user_id: Optional[str] = None
    screen_name: Optional[str] = None
    oauth_callback_confirmed: bool = False

    # Apple附带属性
    username: Optional[str] = None

    # 新版钉钉附带属性 (since 1.16.7)
    corp_id: Optional[str] = None