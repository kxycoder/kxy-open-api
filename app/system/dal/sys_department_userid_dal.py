# coding=UTF-8
import json
from kxy.framework.util import SUtil
from app.common.basedal import BaseDal
from kxy.framework.friendly_exception import FriendlyException
from sqlalchemy import or_, and_, select
# from exts import myredis
from app.database import get_redis_client
from app.system.models.sys_department_info import DepartmentInfo
from app.system.models.sys_department_userid import DepartmentUserid
import re
from datetime import datetime
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)
from app.system.dal.sys_department_info_dal import SysDepartmentInfoDal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List as TypeList

class  SysDepartmentUseridDal(BaseDal[ DepartmentUserid]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__( DepartmentUserid,db,**kwargs)
        self.redis_client = get_redis_client()

    async def get_user_key(self, user_id):
        return 'spider:user_info:{}'.format(user_id)

    # 获取列表
    async def List(self, search, depIds, page_index, page_size, user_type):
        fil = list()

        fil.append(DepartmentUserid.Status != 10)
        if search:
            if re.search(r"^(\d)*$", search):
                fil.append(DepartmentUserid.UserId == int(search))
            else:
                search = search.strip()
                fil.append(or_(DepartmentUserid.UserName.ilike("%" + search + "%"),
                               DepartmentUserid.DepartmentName.ilike("%" + search + "%")))
        if depIds:
            dep_id_list = depIds.split(",")
            fil.append(DepartmentUserid.DepartmentId.in_(dep_id_list))
        if user_type:
            fil.append(DepartmentUserid.UserType == int(user_type))
        return await self.paginate_query(fil, DepartmentUserid.CreateDate.desc(), page_index, page_size)

    async def GetAllActivUser(self):
        return await self.QueryWhere([DepartmentUserid.Status==1])
    # 创建

    async def AddByJsonData(self, jsonData):
        entity = DepartmentUserid()
        entity.InitInsertEntityWithJson(jsonData)
        entity.Status = 1
        await self.Insert(entity)
        return entity

    async def Delete(self, id):
        exist = await self.Get(id)
        if exist != None:
            exist.Status = 10
            await self.Update(exist)
        else:
            raise FriendlyException('不存在' + str(id) + '的数据')

    async def GetNormalUserById(self, id)->DepartmentUserid:
        return await self.QueryOne([DepartmentUserid.UserId == id, DepartmentUserid.UserType == 1])

    async def UpdateByJsonData(self, jsonData):
        id = jsonData.get('Id', None)
        if id == None:
            raise FriendlyException('更新时必须传回主键')
        entity = await self.Get(id)
        if not entity:
            raise FriendlyException('不存在' + str(id) + "的数据")
        entity.InitUpdateFiles(jsonData)
        await self.Update(entity)
        return entity
    async def TrueDelUser(self,userid):
        await self.TrueDelWhere([DepartmentUserid.UserId == userid,DepartmentUserid.UserType == 1])
    async def CreateUser(self, id, phoneNumber, email, chineseName, qywxid, department, departmentName, position,isLeader,sex=None):
        entity = DepartmentUserid()
        entity.UserId = id
        entity.UserName = chineseName
        entity.PhoneNumber = phoneNumber
        entity.Email = email
        entity.QYWXUserId = qywxid
        entity.Status = 1
        entity.UserType = 1
        entity.DepartmentId = department
        entity.DepartmentName = departmentName
        entity.IsLeader = isLeader
        entity.Position = position
        entity.Leader = 0
        if sex:
            entity.Sex = sex
        await self.Insert(entity)
        return entity

    async def SyncData(self, id, username, phoneNumber, email, chineseName, qywxid, department, departmentName, position,isLeader,status):
        entity =await self.GetNormalUserById(id)

        if entity is None:
            if status !=1:
                return
            await self.CreateUser(id, phoneNumber, email, chineseName, qywxid, department, departmentName, position,isLeader)
            logger.info("添加用户%s[%s]"%(chineseName,id))
        else:
            if status !=1:
                logger.info("用户%s[%s]离职被删除"%(chineseName,id))
                await self.TrueDel(entity.Id)
                return
            entity.UserName = chineseName
            entity.PhoneNumber = phoneNumber
            entity.Email = email
            entity.QYWXUserId = qywxid
            entity.Status = 1
            entity.UserType = 1
            entity.DepartmentId = department
            entity.DepartmentName = departmentName
            entity.IsLeader = isLeader
            await self.Update(entity)
    async def UpdateByFields(self,ssoID, phoneNumber, email, chineseName, qywxid, department, departmentName, position,isLeader,leader=None,sex=None):
        entity =await self.GetNormalUserById(ssoID)
        entity.UserId=ssoID
        entity.UserName = chineseName
        entity.PhoneNumber = phoneNumber
        entity.Email = email
        entity.QYWXUserId = qywxid
        entity.UserType = 1
        entity.DepartmentId = department
        entity.DepartmentName = departmentName
        entity.IsLeader = isLeader
        entity.Position = position
        if leader:
            entity.Leader=leader
        if sex:
            entity.Sex = sex
        await self.Update(entity)

    async def UpdateByQYWXUserId(self,QYWXUserId,vpnid):
        entity = await self.QueryOne([DepartmentUserid.QYWXUserId == QYWXUserId,DepartmentUserid.UserType == 1])
        if not entity:
            raise FriendlyException('不存在微信ID为' + str(QYWXUserId) + "的数据")
        entity.VpnId = vpnid
        await self.Update(entity)
        return entity


    async def DeleteUnSync(self):
        now = datetime.now()

        if now.minute > 10:
            minutes = now.minute - 10
        else:
            minutes = 0
        min10 = datetime(now.year, now.month, now.day, now.hour, minutes, now.second)
        await self.TrueDelWhere([DepartmentUserid.LastModifiedDate < min10])
    async def GetUserIdByName(self, name):
        # 根据中文名字查询id
        return self.QueryOne([DepartmentUserid.UserName == name,DepartmentUserid.UserType == 1])

    async def GetUsersByCurrentDepId(self,depId):
        fil = list()
        fil.append(and_(DepartmentUserid.DepartmentId==depId,DepartmentUserid.Status == 1))
        return self.QueryWhere(*fil)

    async def GetDepartmentUseridByDepId(self,depId):
        fil = list()
        fil.append(and_(DepartmentUserid.DepartmentId==depId,DepartmentUserid.Status == 1))
        return self.session.query(DepartmentUserid).filter(*fil)


    async def UpdateDepartmentUserPosition(self,depId,Position):
        users=self.GetDepartmentUseridByDepId(depId)
        self.UpdateEntitiesFields(users, {"Position": Position})
        return users

    async def GetUsersByDepId(self, depId)->TypeList[DepartmentUserid]:
        # 根据部门id查询子部门id
        
        deps = await self.GetDepartmentInfo(depId)
        if deps.Status!=1:
            return []
        # 根据部门id查询用户信息
        return await self.QueryWhere([DepartmentUserid.DepartmentId.in_(deps.ChildIds.split(","))])

    async def GetByUserId(self, userId):
        fil = list()
        fil.append(DepartmentUserid.UserId == userId)
        fil.append(DepartmentUserid.UserType == 1)
        return await self.QueryOne(fil)

    async def GetByUserIdDepId(self, user_id, dep_id):
        fil = list()
        fil.append(DepartmentUserid.UserId == user_id)
        fil.append(DepartmentUserid.DepartmentId == dep_id)
        fil.append(DepartmentUserid.Status != 10)
        return await self.QueryOne(fil)

    async def CheckByUserIdUserType(self, user_id, user_type):
        """
        根据用户id、部门id、用户类型检查是否存在
        """
        fil = list()
        fil.append(DepartmentUserid.UserId == user_id)
        fil.append(DepartmentUserid.UserType == user_type)
        fil.append(DepartmentUserid.Status != 10)
        return await self.QueryOne(fil)

    async def GetByUserName(self, userName):
        fil = list()
        fil.append(DepartmentUserid.UserName == userName)
        return await self.QueryOne(fil)

    async def GetMembersByDepartmentIds(self, department_ids, isAll=0):
        fil = list()
        fil.append(DepartmentUserid.Status == 1)
        if isAll == 0:
            fil.append(DepartmentUserid.DepartmentId.in_(department_ids))
        return await self.QueryWhere(fil)

    async def GetUserByCache(self, user_id):
        user = self.GetByUserId(user_id)
        if user is None:
            return None
        return user.to_basic_dict()

    async def ClearUserCache(self, user_id):
        key = self.get_user_key(user_id)
        return await self.redis_client.delete(key)

    async def ClearAllUserCache(self):
        key = self.get_user_key('')
        return await self.redis_client.delete(key + '*')

    #根据用户ID获取部门名称和部门等级
    async def GetDepartmentByUserIds(self,userIds):
        fil = list()
        fil.append(DepartmentUserid.UserId.in_(userIds))
        fil.append(DepartmentUserid.UserType == 1)
        fields = [DepartmentUserid.UserId,DepartmentInfo.Name,DepartmentInfo.Leve,DepartmentUserid.DepartmentId]
        return self.session.query(DepartmentUserid).outerjoin(DepartmentInfo,DepartmentInfo.Id == DepartmentUserid.DepartmentId). \
            with_entities(*fields).filter(*fil).all()

    # 根据用户ID获取组名和上级部门名称
    async def GetGroupNameAndSuperiorDepNameByUserId(self,userId):
        fil = [DepartmentUserid.UserId == userId, DepartmentUserid.UserType == 1]
        fields = [DepartmentUserid.DepartmentName,DepartmentUserid.DepartmentId]

        personal_info=await self.QueryOne(fil,fields)
        if personal_info:
            dal = SysDepartmentInfoDal(self.UserId, self.session)
            dep_info =await dal.GetUserDepartmentLeve3(personal_info.DepartmentId)
            depName = dep_info.Name
            teamName = "--"
            if dep_info.PrincipalUserId != userId:
                teamName = personal_info.DepartmentName
            return teamName,depName
        else:
            return "--","--"

    async def GetNameByUserId(self, userId):
        result = await self.QueryOne([DepartmentUserid.UserId == userId],[DepartmentUserid.UserName])
        return result.UserName

    async def GetBatchNameByUserId(self, userIds):
        fields = [DepartmentUserid.UserId,DepartmentUserid.UserName,DepartmentUserid.Email]
        return await self.QueryWhere([DepartmentUserid.UserId.in_(userIds)],fields)
    async def GetBatchActiveNameByUserId(self, userIds):
        fields = [DepartmentUserid.UserId,DepartmentUserid.UserName,DepartmentUserid.Email]
        return await self.QueryWhere([DepartmentUserid.UserId.in_(userIds),DepartmentUserid.Status==1],fields)
    async def GetUsersByDepartmentId(self, depId):
        # 根据部门id查询部门所有用户
        return await self.QueryWhere([DepartmentUserid.DepartmentId == depId])
    async def BatchGetUsersByDepIds(self,depIds):
        # 根据多个部门Id查询信息，depIds为列表类型
        return await self.QueryWhere([DepartmentUserid.DepartmentId.in_(depIds)])

    async def GetChildUsers(self, user_id=None):
        if user_id is None:
            user_id = self.UserId
        user = await self.GetUser(user_id,1)
        department = await self.GetDepartmentInfo(user.DepartmentId)
        childs = department.ChildIds
        if childs:
            childs = childs.split(',')
        else:
            childs = []
        child_users = await self.QueryWhere(DepartmentUserid.DepartmentId.in_(childs))
        return SUtil.formatListData(child_users)

    async def GetChildUserIds(self, user_id=None):
        data =await self.GetChildUsers(user_id)
        return [item['UserId'] for item in data]
    async def GetUser(self,userid,userType=None)->DepartmentUserid:
        fil = [DepartmentUserid.UserId==userid]
        if userType:
            fil.append(DepartmentUserid.UserType==userType)
        return await self.QueryOne(fil)
    async def GetDepartmentMembers(self, user_id=None):
        if user_id is None:
            user_id = self.UserId
        
        user = await self.GetUser(user_id,1)
        department =await self.GetDepartmentInfo([DepartmentInfo.Id == user.DepartmentId])
        if user_id == department.PrincipalUserId:
            childs = department.ChildIds.split(',')
            members = await self.GetMembersByDepartmentIds(childs)
            members = [item.UserId for item in members]
        else:
            members = [user_id]
        return members

    async def GetPrincipalUserId(self, user_id:int):
        user = await self.GetUser(user_id, 1)
        department = await self.GetDepartmentInfo(user.DepartmentId)
        if department is not None:
            return department.PrincipalUserId
        return None
    async def GetDepartmentInfo(self,departmentId)->DepartmentInfo:
        department =await self.session.execute(select(DepartmentInfo).filter(DepartmentInfo.Id == departmentId).limit(1))
        await self.session.commit()
        department = department.scalars().first()
        return department
    async def GetLeaderInfo(self, user_id, leader_info=None, level=5):
        if leader_info is None:
            leader_info = []
        user:DepartmentUserid = self.QueryOne([DepartmentUserid.UserId == user_id])
        if not user:
            return leader_info
        department = await self.GetDepartmentInfo(user.DepartmentId)
        if department is None:
            raise FriendlyException(f'用户{user.UserName}部门{user.DepartmentId}不存在')
        leader_id = department.PrincipalUserId
        if leader_id:
            leader =await self.QueryOne([DepartmentUserid.UserId == leader_id])
            if leader:
                leader_info.append(leader)
            else:
                return leader_info
            if department.Leve <= 3:
                return leader_info
            parent_department =await self.GetDepartmentInfo(department.ParentId)
            user_id = parent_department.PrincipalUserId
            user =await self.GetUser(user_id)
            if user:
                leader_info.append(user)
        else:
            return leader_info
        level -= 1
        if level <= 3 or parent_department.Leve <= 3 or user_id is None:
            return leader_info
        return await self.GetLeaderInfo(user_id, leader_info, level)

    async def GetParentLeader(self, department_id):
        department = await self.GetDepartmentInfo(department_id)
        parent_department = await self.GetDepartmentInfo(department.ParentId)
        parent_department = parent_department.scalars().first()
        return parent_department.PrincipalUserId

    async def DeleteBySSOId(self,ssoid):
        entity =await self.QueryOne([DepartmentUserid.UserId ==ssoid])
        if entity is not None:
            entity.Status=10
            await self.Update(entity)
        return entity

    async def GetAllUserNameByUserIds(self, userIds):
        """
        根据userId获取用户名
        """
        fil = list()
        fil.append(DepartmentUserid.UserId.in_(userIds))
        fil.append(DepartmentUserid.Status != 10)
        return await self.QueryWhere(fil,fields=[DepartmentUserid.UserName])

    async def GetUserIdByPosition(self, Position):
        """
        根据岗位查出user_id
        """
        return await self.QueryWhere(fil=[DepartmentUserid.Position == Position],fields=[DepartmentUserid.UserId])

    async def GetPositionByUserId(self, UserId):
        """
        根据UserId查出岗位
        """
        return await self.QueryOne(fil=[DepartmentUserid.UserId == UserId],fields=[DepartmentUserid.Position])

    async def GetUserInfoByDepId(self, DepId):
        """
        根据部门Id获取用户
        """
        return await self.QueryOne(fil=[DepartmentUserid.DepartmentId == DepId])

    async def GetUserInfoByUserIds(self, UserIds):
        """
        根据UserIds获取相关信息
        """
        return await self.QueryWhere(fil=[DepartmentUserid.UserId.in_(UserIds)])
        
