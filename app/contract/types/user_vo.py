from typing import Dict, List
from pydantic import BaseModel
class VoUserInfo(BaseModel):
    id:int
    password:str

class VoUserProfilePass(BaseModel):
    newPassword: str
    oldPassword: str

    
# {"userId":141,"roleIds":[101,1]}# 
class VoUserRole(BaseModel):
    userId:int
    roleIds:list

# {"name":"测试租户名","packageId":112,"contactName":"张三","contactMobile":"1860165373","accountCount":1000,"expireTime":1756396800000,"website":"www.baidu.com","status":0,"username":"fsdfdsf","password":"sdfsfsdf"}
# 
class VoUserTenant(BaseModel):
    name:str
    packageId:int
    contactName:str
    contactMobile:str = ''
    contactUserId:int = 0
    accountCount:int=10
    expireTime:int=10000
    website:str=''
    status:int=0
    username:str
    password:str

# {"content":"{code}胜多负少答复收到","params":["code"],"mobile":"","templateCode":"test1","templateParams":{"code":"胜多负少答复收到"},"userType":2,"userId":112}
class VoSendNotify(BaseModel):
    content:str
    params:List[str]
    mobile:str = ''
    templateCode:str
    templateParams:Dict[str,str]
    userType:int
    userId:int