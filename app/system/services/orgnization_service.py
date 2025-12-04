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

    async def sync_departments_to_system_dept(self) -> Dict:
        """
        同步企业微信部门到SystemDept
        
        Returns:
            Dict: 同步结果信息
        """
        # 获取企业微信部门列表
        dept_result =await user_system_util.list_departments(1)
        
        if dept_result.get('errcode') != 0:
            raise FriendlyException(f"获取企业微信部门失败: {dept_result.get('errmsg')}")
        
        departments = dept_result.get('departments', dept_result.get('department', []))
        
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
        for dept in departments:
            dept_id = dept.get('id')
            dept_name = dept.get('name')
            parent_id = dept.get('parentId') if 'parentId' in dept else dept.get('parentid')
            
            # 如果部门已存在，则更新；否则创建新部门
            if str(dept_id) in existing_dept_dict:
                # 更新现有部门
                system_dept = existing_dept_dict[str(dept_id)]
                system_dept.name = dept_name
                system_dept.parentId = parent_id
                system_dept.updater = "system"
                system_dept.deleted = 0
                
                await dept_dal.Update(system_dept)
                stats['updated'] += 1
            else:
                # 创建新部门
                system_dept = SystemDept()
                system_dept.id = dept_id
                system_dept.name = dept_name
                system_dept.parentId = parent_id
                system_dept.sort = 0
                system_dept.status = 0  # 默认启用
                system_dept.creator = "system"
                system_dept.updater = "system"
                system_dept.tenantId = 1  # 默认租户
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

        user_result = await user_system_util.list_users(1, 1)
        if user_result.get('errcode') != 0:
            raise FriendlyException(f"获取用户列表失败: {user_result.get('errmsg')}")

        remote_users = user_result.get('userlist', []) or []
        if not remote_users:
            return {"success": True, "message": "无可同步的用户"}

        user_dal = SystemUsersDal(self.session)
        dept_dal = SystemDeptDal(self.session)
        role_dal = SystemUserRoleDal(self.session)
        crypto = Crypto()
        tenant_id = self.tenantId or 1

        existing_users = await user_dal.QueryWhere([SystemUsers.deleted == 0])
        existing_user_dict = {user.username: user for user in existing_users}

        departments = await dept_dal.QueryWhere([SystemDept.deleted == 0])
        dept_dict = {int(dept.id): dept for dept in departments if dept.id is not None}

        stats = {'created': 0, 'updated': 0, 'ignored': 0}

        def normalize_dept_id(raw_value):
            if raw_value is None:
                return None
            if isinstance(raw_value, list):
                for item in raw_value:
                    normalized = normalize_dept_id(item)
                    if normalized is not None:
                        return normalized
                return None
            if isinstance(raw_value, str) and raw_value.strip().startswith('['):
                try:
                    parsed = json.loads(raw_value)
                    return normalize_dept_id(parsed)
                except Exception:
                    return None
            if isinstance(raw_value, str) and ',' in raw_value:
                return normalize_dept_id([part.strip() for part in raw_value.split(',') if part.strip()])
            try:
                return int(raw_value)
            except (TypeError, ValueError):
                return None

        def extract_username(user):
            for key in ('userid', 'userId', 'id', 'username'):
                value = user.get(key)
                if value:
                    return str(value)
            fallback = user.get('mobile') or user.get('phone') or user.get('tel')
            return str(fallback) if fallback else None

        def extract_dept_id(user):
            dept_fields = ('dept_id_list', 'deptIdList', 'department', 'departments')
            for field in dept_fields:
                raw = user.get(field)
                if raw:
                    return normalize_dept_id(raw)
            return None

        def extract_status(user):
            status_value = user.get('status')
            if isinstance(status_value, int):
                return 0 if status_value in (0, 1) else 1
            active = user.get('active')
            if isinstance(active, bool):
                return 0 if active else 1
            return 0

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

        def generate_password(user):
            base_value = user.get('mobile') or user.get('userid') or user.get('userId') or '123456'
            return str(base_value)

        for remote_user in remote_users:
            username = extract_username(remote_user)
            if not username:
                stats['ignored'] += 1
                continue

            nickname = remote_user.get('name') or remote_user.get('nickname') or username
            dept_id = extract_dept_id(remote_user)
            email = remote_user.get('email') or remote_user.get('biz_mail')
            mobile = remote_user.get('mobile') or remote_user.get('phone') or remote_user.get('tel')
            avatar = remote_user.get('thumb_avatar') or remote_user.get('avatar')
            remark = remote_user.get('position') or remote_user.get('title')
            status = extract_status(remote_user)

            existing_user = existing_user_dict.get(username)
            if existing_user:
                existing_user.nickname = nickname
                existing_user.deptId = dept_id
                existing_user.email = email
                existing_user.mobile = mobile
                existing_user.avatar = avatar
                existing_user.status = status
                existing_user.remark = remark
                existing_user.updater = 'system'
                existing_user.deleted = 0
                await user_dal.Update(existing_user)
                stats['updated'] += 1
            else:
                new_user = SystemUsers()
                new_user.username = username
                new_user.nickname = nickname
                new_user.password = crypto.encrypt(generate_password(remote_user))
                new_user.deptId = dept_id
                new_user.email = email
                new_user.mobile = mobile
                new_user.avatar = avatar
                new_user.status = status
                new_user.remark = remark
                new_user.creator = 'system'
                new_user.updater = 'system'
                new_user.tenantId = tenant_id
                new_user.deleted = 0
                await user_dal.Insert(new_user)
                existing_user_dict[username] = new_user
                stats['created'] += 1

                role_ids = extract_roles_from_dept(dept_id)
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
