from pydantic import BaseModel
from typing import Optional, List


class DepartmentVO(BaseModel):
    """
    标准化的部门实体类，用于统一不同来源渠道的部门数据
    """
    # 部门唯一标识符
    id: int
    
    # 部门名称
    name: str
    
    # 父级部门ID
    parent_id: int
    
    # 部门层级
    level: Optional[int] = None
    
    # 部门负责人ID
    principal_user_id: Optional[int] = None
    
    # 部门负责人姓名
    principal_user_name: Optional[str] = None
    
    # 子部门ID列表
    child_ids: Optional[List[int]] = None
    
    # 部门类型
    dep_type: Optional[str] = None
    
    # 部门排序
    sort: Optional[int] = None
    
    # 部门状态 (0-启用, 1-禁用)
    status: Optional[int] = 0
    
    # 创建者
    creator: Optional[str] = None
    
    # 更新者
    updater: Optional[str] = None
    
    # 租户ID
    tenant_id: Optional[int] = None


class UserVO(BaseModel):
    """
    标准化的用户实体类，用于统一不同来源渠道的用户数据
    """
    # 用户唯一标识符
    user_id: str
    
    # 用户名
    username: str
    
    # 昵称/中文名
    nickname: str
    
    # 手机号码
    mobile: Optional[str] = None
    
    # 邮箱
    email: Optional[str] = None
    
    # 所属部门ID
    department_id: Optional[int] = None
    
    # 所属部门名称
    department_name: Optional[str] = None
    
    # 职位
    position: Optional[str] = None
    
    # 是否为上级/领导
    is_leader: Optional[bool] = False
    
    # 头像
    avatar: Optional[str] = None
    
    # 性别
    gender: Optional[int] = None
    
    # 状态 (0-在职, 1-离职)
    status: Optional[int] = 0
    
    # 备注
    remark: Optional[str] = None
    
    # 创建者
    creator: Optional[str] = None
    
    # 更新者
    updater: Optional[str] = None
    
    # 租户ID
    tenant_id: Optional[int] = None