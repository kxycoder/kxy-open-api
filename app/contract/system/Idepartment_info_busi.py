# 接口文件 (基于 department_info_busi.py 生成)

from abc import ABC, abstractmethod


class IDepartmentInfoBusi(ABC):
    @abstractmethod
    async def sync_from_sso(self):
        pass

    @abstractmethod
    async def sync_users_from_sso(self):
        pass

    @abstractmethod
    async def sync_department_to_oa(self):
        pass

    @abstractmethod
    async def sysnc_users_to_oa(self):
        pass

    @abstractmethod
    async def sync_username(self, username):
        pass

    @abstractmethod
    async def sysnc_user_to_oa(self, user):
        pass

    @abstractmethod
    async def sync_postion_to_oa(self):
        pass

    @abstractmethod
    async def sync_leader_from_sso(self):
        pass

    @abstractmethod
    async def StartSetLeader(self):
        pass

    @abstractmethod
    async def SetLeader(self, departments, leader):
        pass

    @abstractmethod
    async def add_user(self, json_data):
        pass

    @abstractmethod
    async def get_department_and_users(self, roles=None):
        pass

    @abstractmethod
    async def get_user_info(self, user_id=None, dep_id=None, roles=None):
        pass

    @abstractmethod
    async def get_follow_departments(self, brand_id, order_type):
        pass

    @abstractmethod
    async def get_department_info(self, DepId):
        pass

    @abstractmethod
    async def get_department_info_byId(self, DepId):
        pass

    @abstractmethod
    async def get_manage_department(self, user_dal, department_dal, brand_pk_id, role_id, name):
        pass

    @abstractmethod
    async def get_users_by_department_id(self):
        pass

    @abstractmethod
    async def sync_departmentuserid_position_to_oa(self, DepartmentId, Position):
        pass

    @abstractmethod
    async def get_responsible_leader(self, userId):
        pass

    @abstractmethod
    async def depInfo_by_userId_leve(self, userId, Leve):
        pass

    @abstractmethod
    async def getLeve3DepInfo(self, ParentId):
        pass

    @abstractmethod
    async def getSubDepByIds(self, depIds):
        pass

    @abstractmethod
    async def getSubMembersByIds(self, depIds, userId):
        pass

    @abstractmethod
    async def get_batch_by_userId(self, userIds):
        pass

    @abstractmethod
    async def getParentDep(self, UserId):
        pass

    @abstractmethod
    async def get_child_members(self, department_id):
        pass

    @abstractmethod
    async def getResponsibleDeps(self, depIds, userId):
        pass

    @abstractmethod
    async def get_dep_trees(self):
        pass

    @abstractmethod
    async def get_members_by_depId(self, depId):
        pass

    @abstractmethod
    async def get_deps_by_userId(self, UserId):
        pass

    @abstractmethod
    async def get_dep_upper(self, depId, res):
        pass

    @abstractmethod
    async def get_depInfo_by_depType(self, depId):
        pass

    @abstractmethod
    async def get_user_first_department(self, userId):
        pass

    @abstractmethod
    async def getIsLeader(self, userId):
        pass

    @abstractmethod
    async def get_user_leve2_dep(self, depId):
        pass

    @abstractmethod
    async def getUserCenterInfo(self, userId):
        pass

    @abstractmethod
    async def get_user_all_dep(self, depId, depLeve, dep_list):
        pass

    @abstractmethod
    async def getUserAllDep(self, userId, depLeve):
        pass

    @abstractmethod
    async def getOkrInfo(self, userId):
        pass

    @abstractmethod
    async def get_members_by_ids(self, ids):
        pass

