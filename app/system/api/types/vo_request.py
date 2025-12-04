# {"tenantName":"快享云源码","nickname":"used","tenantId":0,"username":"user","password":"123456","confirmPassword":"123456"}
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class VoRegistTenant(BaseModel):
    tenantName: Optional[str] = Field(None, title="租户名称")
    nickname: Optional[str] = Field(None, title="昵称")
    tenantId: Optional[int] = Field(None, title="租户编号")
    username: Optional[str] = Field(None, title="用户名")
    password: Optional[str] = Field(None, title="密码")
    confirmPassword: Optional[str] = Field(None, title="确认密码")


class VoSocialUser(BaseModel):
    rawUserInfo: Optional[dict] = Field(title="原始用户数据")
    unionid: Optional[str] = Field(title="用户唯一标识") 
    nickname: Optional[str] = Field(title="用户昵称",default="")
    username: Optional[str] = Field(title="用户名",default="")
    gender: Optional[str] = Field(title="性别",default="")
    source: Optional[str] = Field(title="来源",default="")
    rawToken: Optional[dict] = Field(title="rawToken")
    token: Optional[str] = Field(title="token",default="")
    code: Optional[str] = Field(title="code",default="")
    state: Optional[str] = Field(title="state",default="")
    avatar: Optional[str] = Field(title="头像",default="")
    qyId: Optional[str] = Field(title="企业微信id",default="")
    tenantId: Optional[int] = Field(title="租户编号",default=0)
    phone: Optional[str] = Field(title="手机号",default="")
    email: Optional[str] = Field(title="邮箱",default="")
    department: Optional[str] = Field(title="部门",default="")
# {"type":"20","code":"06562527cabf33b9a88d4dd601a46bea","state":"4789fe9dd387443e996d9c14e5398289"}
class VoSocialAuthRedirect(BaseModel):
    type: Optional[str] = Field(title="类型")
    code: Optional[str] = Field(None, title="code")
    state: Optional[str] = Field(None, title="state")
    token: Optional[str] = Field(None, title="token")