from app.contract.infra.Iconfig_service import IConfigService
from app.system.services.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from app.vendor.base_message_util import MessageUtilBase
from app.vendor.wechat_work_util import WeChatWorkUtil
from app.vendor.dingtalsk_util import DingTalkUtil
from app.system.dal.system_dept_dal import SystemDeptDal
from app.system.dal.system_user_role_dal import SystemUserRoleDal
from app.system.dal.system_users_dal import SystemUsersDal
from app.system.models.system_dept import SystemDept
from app.system.models.system_users import SystemUsers
from app.contract.types.user_vo import VoUserRole
from app.contract.types.department_vo import DepartmentVO, UserVO
from app.common.crypto_util import Crypto
from kxy.framework.friendly_exception import FriendlyException
from typing import List, Dict
from kxy.framework.mapper import Mapper
import app.global_var as global_var
import json

user_system_util:MessageUtilBase = None
class OrgnizationService(BaseService):
    def __init__(self, db: AsyncSession, require_user_system_util: bool = True, **kwargs):
        super().__init__(db, **kwargs)
        if require_user_system_util and not user_system_util:
            raise FriendlyException("请先初始化用户系统工具类")
    @classmethod
    async def initialize_user_system_util(cls, session,reload=False)->MessageUtilBase:
        """
        异步初始化用户系统工具类
        该方法应在应用启动时调用，确保只初始化一次
        """
        global user_system_util
        if reload or user_system_util is None:
            configSvc = Mapper.getservice_by_contract(IConfigService, session)
            # 异步获取配置
            user_resource_type = await configSvc.Get('sys.usersource.channel')
            # 获取appkey和appsec参数并设置到工具类实例中
            app_key = await configSvc.Get(f'sys.usersource.channel.appkey')
            app_sec = await configSvc.Get(f'sys.usersource.channel.appsec')
            
            # 根据配置选择对应的工具类
            if user_resource_type == 'qywx':
                user_system_util = WeChatWorkUtil(app_key,app_sec)
            elif user_resource_type == 'dingtalk':
                user_system_util = DingTalkUtil(app_key,app_sec)
            else:
                # 默认使用企业微信
                user_system_util = WeChatWorkUtil(app_key,app_sec)
        return user_system_util


    async def convert_to_standard_user(self, source_user: dict) -> UserVO:
        """
        将不同来源的用户数据转换为标准的UserVO对象
        
        Args:
            source_user: 来源于不同系统的用户原始数据
            
        Returns:
            UserVO: 标准化的用户对象
        """
        # 根据不同平台做字段映射
        if hasattr(user_system_util, 'platform') and user_system_util.platform == 'dingtalk':
            # 钉钉平台字段映射
            user_id = source_user.get('userid')
            username = source_user.get('userid')
            nickname = source_user.get('name')
            mobile = source_user.get('mobile')
            email = source_user.get('email')
            department_id = source_user.get('department')
            position = source_user.get('position')
            is_leader = bool(source_user.get('is_leader'))
            avatar = source_user.get('avatar')
            gender = source_user.get('gender')
            status = 0 if source_user.get('active') else 1
        else:
            # 默认为企业微信平台字段映射
            user_id = source_user.get('userid')
            username = source_user.get('userid')
            nickname = source_user.get('name')
            mobile = source_user.get('mobile')
            email = source_user.get('email') or source_user.get('biz_mail')
            department_id = source_user.get('department')
            position = source_user.get('position')
            is_leader = bool(source_user.get('isleader'))
            avatar = source_user.get('thumb_avatar') or source_user.get('avatar')
            gender = source_user.get('gender')
            status = 0 if source_user.get('status') == 1 else 1
            
        # 创建标准用户VO对象
        user_vo = UserVO(
            user_id=user_id,
            username=username,
            nickname=nickname,
            mobile=mobile,
            email=email,
            department_id=department_id[0] if isinstance(department_id, list) and len(department_id) > 0 else department_id,
            department_name=source_user.get('department_name'),
            position=position,
            is_leader=is_leader,
            avatar=avatar,
            gender=gender,
            status=status,
            remark=source_user.get('alias') or source_user.get('telephone'),
            creator="system",
            updater="system",
            tenant_id=self.tenantId or 1
        )
        
        return user_vo

    async def sync_departments_to_system_dept(self) -> Dict:
        """
        同步企业微信部门到SystemDept
        
        Returns:
            Dict: 同步结果信息
        """
        # 获取企业微信部门列表
        departments =await user_system_util.list_departments(1)
        
        if not departments:
            raise FriendlyException(f"获取企业微信部门失败")
        
        # 获取现有的SystemDept部门列表
        dept_dal = SystemDeptDal(self.session)
        existing_depts = await dept_dal.QueryWhere([])
        existing_dept_dict = {str(dept.id): dept for dept in existing_depts}
        
        # 统计信息
        stats = {
            'created': 0,
            'updated': 0,
            'ignored': 0
        }
        
        # 处理每个企业微信部门
        for standard_dept in departments:
            
            # 如果部门已存在，则更新；否则创建新部门
            if str(standard_dept.id) in existing_dept_dict:
                # 更新现有部门
                system_dept = existing_dept_dict[str(standard_dept.id)]
                system_dept.name = standard_dept.name
                system_dept.parentId = standard_dept.parent_id
                system_dept.updater = standard_dept.updater
                system_dept.deleted = 0
                
                await dept_dal.Update(system_dept)
                stats['updated'] += 1
            else:
                # 创建新部门
                system_dept = SystemDept()
                system_dept.id = standard_dept.id
                system_dept.name = standard_dept.name
                system_dept.parentId = standard_dept.parent_id
                system_dept.sort = standard_dept.sort or 0
                system_dept.status = standard_dept.status or 0  # 默认启用
                system_dept.creator = standard_dept.creator
                system_dept.updater = standard_dept.updater
                system_dept.tenantId = standard_dept.tenant_id or 1  # 默认租户
                system_dept.deleted = 0
                
                await dept_dal.Insert(system_dept)
                stats['created'] += 1
        
        return {
            "success": True,
            "message": f"同步完成，新增{stats['created']}个部门，更新{stats['updated']}个部门，忽略{stats['ignored']}个部门"
        }
    async def sync_users_to_system_users(self) -> Dict:
        """同步外部用户到SystemUsers表，并在创建时自动授予默认角色"""

        if not user_system_util:
            raise FriendlyException("用户系统工具类未初始化")

        remote_users = await user_system_util.list_users(1, 1)
        if not remote_users:
            raise FriendlyException(f"获取用户列表失败")

        user_dal = SystemUsersDal(self.session)
        dept_dal = SystemDeptDal(self.session)
        role_dal = SystemUserRoleDal(self.session)
        crypto = Crypto()
        tenant_id = self.tenantId

        existing_users = await user_dal.QueryWhere([SystemUsers.deleted == 0])
        existing_user_dict = {user.username: user for user in existing_users}

        departments = await dept_dal.QueryWhere([SystemDept.deleted == 0])
        dept_dict = {int(dept.id): dept for dept in departments if dept.id is not None}

        stats = {'created': 0, 'updated': 0, 'ignored': 0}

        def extract_roles_from_dept(dept_id):
            visited = set()
            current = dept_id
            while current and current not in visited:
                visited.add(current)
                try:
                    dept_key = int(current)
                except (TypeError, ValueError):
                    break
                dept = dept_dict.get(dept_key)
                if not dept:
                    break

                roles = dept.defaultRoles
                if isinstance(roles, list) and roles:
                    normalized = []
                    for role in roles:
                        try:
                            normalized.append(int(role))
                        except (TypeError, ValueError):
                            continue
                    if normalized:
                        return normalized
                current = dept.parentId
            return []

        def generate_password(user:UserVO):
            base_value = user.mobile or user.user_id or user.user_id or '123456'
            return str(base_value)

        for standard_user in remote_users:
            existing_user = existing_user_dict.get(standard_user.username)
            if existing_user:
                existing_user.nickname = standard_user.nickname
                existing_user.deptId = standard_user.department_id
                existing_user.email = standard_user.email
                existing_user.mobile = standard_user.mobile
                existing_user.avatar = standard_user.avatar
                existing_user.status = standard_user.status
                existing_user.remark = standard_user.remark
                existing_user.updater = standard_user.updater
                existing_user.deleted = 0
                await user_dal.Update(existing_user)
                stats['updated'] += 1
            else:
                new_user = SystemUsers()
                new_user.username = standard_user.user_id
                new_user.nickname = standard_user.nickname
                new_user.password = crypto.encrypt(generate_password(standard_user))
                new_user.deptId = standard_user.department_id
                new_user.email = standard_user.email
                new_user.mobile = standard_user.mobile
                new_user.avatar = standard_user.avatar
                new_user.status = standard_user.status
                new_user.remark = standard_user.remark
                new_user.creator = standard_user.creator
                new_user.updater = standard_user.updater
                new_user.tenantId = standard_user.tenant_id or tenant_id
                new_user.deleted = 0
                await user_dal.Insert(new_user)
                existing_user_dict[standard_user.username] = new_user
                stats['created'] += 1

                role_ids = extract_roles_from_dept(standard_user.department_id)
                if role_ids:
                    await role_dal.AssignUserRole(VoUserRole(userId=new_user.id, roleIds=role_ids), tenantId=tenant_id)

        return {
            "success": True,
            "message": f"同步完成，新增{stats['created']}个用户，更新{stats['updated']}个用户，忽略{stats['ignored']}个用户"
        }

    async def delete_departments_with_children(self, dept_ids: List[int]) -> int:
        """
        删除指定部门及其所有子部门
        Args:
            dept_ids (List[int]): 需要删除的部门ID列表
        Returns:
            int: 实际删除的部门数量
        """
        if isinstance(dept_ids, int):
            dept_ids = [dept_ids]
        elif isinstance(dept_ids, str):
            dept_ids = [item.strip() for item in dept_ids.split(',') if item.strip()]
        elif not isinstance(dept_ids, list):
            dept_ids = list(dept_ids)

        normalized_ids: List[int] = []
        for dept_id in dept_ids:
            if dept_id is None:
                continue
            if isinstance(dept_id, str):
                dept_id = dept_id.strip()
                if not dept_id:
                    continue
                if ',' in dept_id:
                    for split_id in [part.strip() for part in dept_id.split(',') if part.strip()]:
                        try:
                            normalized_ids.append(int(split_id))
                        except (TypeError, ValueError):
                            raise FriendlyException("部门编号必须为数字")
                    continue
            try:
                normalized_ids.append(int(dept_id))
            except (TypeError, ValueError):
                raise FriendlyException("部门编号必须为数字")

        if not normalized_ids:
            raise FriendlyException("请传入要删除的部门")

        dept_dal = SystemDeptDal(self.session)
        ids_to_delete = set(normalized_ids)
        queue = list(ids_to_delete)

        while queue:
            child_rows = await dept_dal.QueryWhere([
                SystemDept.parentId.in_(queue),
                SystemDept.deleted == 0
            ])
            queue = []
            for child in child_rows:
                child_id = int(child.id)
                if child_id not in ids_to_delete:
                    ids_to_delete.add(child_id)
                    queue.append(child_id)

        await dept_dal.DeleteBatch(list(ids_to_delete))
        return len(ids_to_delete)