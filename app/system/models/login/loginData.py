from pydantic import BaseModel, Field
from typing import Optional

class LoginData(BaseModel):
    clinet_type: str = Field(..., description="客户端类型")
    token: str = Field(..., description="token")
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    secret_id: str = Field(..., description="密钥ID")
    secret_key: str = Field(..., description="密钥")