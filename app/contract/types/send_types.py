from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
# {
#                 "biz_id":response.body.biz_id,
#                 "code":response.body.code,
#                 "message":response.body.message,
#                 "request_id":response.body.request_id
#             }
class SenderReturnModal(BaseModel):
    code:str
    message:str
    requestId:str
    serialNo:str
    
class MessageCallbackModal(BaseModel):
    send_time: Optional[str] = Field(None, description="发送时间")
    report_time: Optional[str] = Field(None, description="回执时间")
    success: bool = Field(..., description="是否成功")
    err_msg: Optional[str] = Field(None, description="错误信息")
    err_code: Optional[str] = Field(None, description="错误代码")
    phone_number: str = Field(..., description="手机号")
    sms_size: Optional[str] = Field(None, description="短信大小")
    requestId: str = Field(..., description="请求编号")
    out_id: Optional[str] = Field(None, description="外部编号")  # 可选字段
    
# {"content":"您的验证码为：{code}，请勿泄露于他人！","params":["code"],"mobile":"18601650373","templateCode":"login","templateParams":{"code":"456142"}}
from pydantic import BaseModel, Field
from typing import Optional
class SmsTestObject(BaseModel):
    """
    短信模板
    """
    content:str
    params:list[str]
    mobile:str
    templateCode:str
    templateParams:Optional[dict] = Field(None, description="模板参数")

class condtion(BaseModel):
    """
    查询条件
    """
    key:str
    oprator:str = ''
    value:Any = ''

class QueryLogFileObject(BaseModel):
    """
    查询日志文件
    """
    filters:List[condtion] = []
    start_time:str = ''
    end_time:str = ''