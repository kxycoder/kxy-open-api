# coding=UTF-8

from app.common.basedal import BaseDal
from kxy.framework.friendly_exception import FriendlyException
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.system.models.sys_department_info import DepartmentInfo
import re
from datetime import datetime
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)



class SysDepartmentInfoDal(BaseDal[DepartmentInfo]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__(DepartmentInfo,db,**kwargs)

    # 获取列表
    async def List(self, search, page_index, page_size):
        fil = list()

        fil.append(DepartmentInfo.Status != 10)
        if search:
            if re.search(r"^(\d)*$", search):
                fil.append(or_(DepartmentInfo.Id == int(search), DepartmentInfo.ParentId == int(search)))
            else:
                search = search.strip()
                fil.append(or_(DepartmentInfo.Name.ilike("%" + search + "%"),
                               DepartmentInfo.PrincipalUserName.ilike("%" + search + "%")))
        return await self.paginate_query(fil, DepartmentInfo.CreateDate.desc(), page_index, page_size)
    # 获取所有的数据
    async def AllList(self):
        fil = list()
        fil.append(DepartmentInfo.Status != 10)
        return await self.QueryWhere(fil)

    # 创建
    async def Search(self,search,leve,parentId, page_index, page_size):
        fil = list()

        fil.append(DepartmentInfo.Status != 10)
        if leve!=0:
            fil.append(DepartmentInfo.Leve==leve)
        if parentId!=None:
            fil.append(DepartmentInfo.ParentId==parentId)
        if search:
           if re.search(r"^(\d)*$", search):
               fil.append(DepartmentInfo.Id == int(search))
           else:
               search =search.strip()
               fil.append(DepartmentInfo.Name.ilike("%" + search + "%"))
        return await self.paginate_query(fil, DepartmentInfo.CreateDate.desc(), page_index, page_size)

    async def AddByJsonData(self, jsonData):
        entity = DepartmentInfo()
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

    async def UpdateByJsonData(self, jsonData,olddata=False):
        id = jsonData.get('Id', None)
        if id == None:
            raise FriendlyException('更新时必须传回主键')
        entity = await self.Get(id)
        if not entity:
            raise FriendlyException('不存在' + str(id) + "的数据")
        if olddata:
            oldPrincipalUserName=entity.PrincipalUserName
            oldPosition=entity.Position
            entity.InitUpdateFiles(jsonData)
            await self.Update(entity)
            return entity,oldPrincipalUserName,oldPosition
        entity.InitUpdateFiles(jsonData)
        await self.Update(entity)
        return entity

    async def SyncData(self, id, name, parentId, leve, childIDs,status):
        entity = await self.Get(id)
        if entity == None:
            if status !=1:
                return
            entity = DepartmentInfo()
            entity.Id = id
            entity.Name = name
            entity.ParentId = parentId
            entity.Leve = leve
            entity.Status = 1
            entity.ChildIds = childIDs
            await self.Insert(entity)
        else:
            if status !=1:
                logger.info("部门%s[%s]删除"%(name,id))
                await self.TrueDel(entity.Id)
                return
            entity.Name = name
            entity.ParentId = parentId
            entity.Leve = leve
            entity.Status = 1
            entity.ChildIds = childIDs
            await self.Update(entity)
        return entity
                
    async def DeleteUnSync(self):
        now = datetime.now()
        if now.minute>10:
            minutes = now.minute-10
        else:
            minutes=0
        min10 = datetime(now.year, now.month, now.day, now.hour, minutes, now.second)
        self.session.query(DepartmentInfo).filter(DepartmentInfo.LastModifiedDate < min10).delete()

    async def GetAll(self):
        return self.QueryWhere([])

    async def GetByIds(self, department_ids):
        fil = list()
        fil.append(DepartmentInfo.Id.in_(department_ids))
        fil.append(DepartmentInfo.Status != 10)
        return await self.QueryWhere(fil)

    async def GetChildDepartments(self, department_id):
        fil = list()
        fil.append(DepartmentInfo.Id == department_id)
        fil.append(DepartmentInfo.Status != 10)
        department = await self.QueryOne(fil)
        if department is None:
            return []
        if department.ChildIds is None:
            return []
        return [int(item) for item in department.ChildIds.split(',')]

    async def GetMultiChildDepartments(self, department_ids):
        fil = list()
        fil.append(DepartmentInfo.Id.in_(department_ids))
        fil.append(DepartmentInfo.Status != 10)
        departments = self.session.query(DepartmentInfo).filter(*fil).all()
        childs = []
        for department in departments:
            childs += department.ChildIds.split(',')
        return childs

    async def GetDepartmentsByParentId(self, parent_department_id, level=3):
        fil = list()
        fil.append(DepartmentInfo.Leve == level)
        fil.append(DepartmentInfo.ParentId == parent_department_id)
        fil.append(DepartmentInfo.Status != 10)
        return await self.QueryWhere(fil)

    async def GetDepartmentByParentId(self, parent_department_id):
        fil = list()
        fil.append(DepartmentInfo.Id == parent_department_id)
        fil.append(DepartmentInfo.Status != 10)
        return await self.QueryOne(fil)

    async def GetDepartmentsByLevel(self, level=4, department_ids=None):
        fil = list()
        if department_ids and type(department_ids) == list:
            fil.append(DepartmentInfo.Id.in_(department_ids))
        fil.append(DepartmentInfo.Leve == level)
        fil.append(DepartmentInfo.Status != 10)
        return await self.QueryWhere(fil)

    async def GetUserDepartment(self, department_id):
        fil = list()
        fil.append(DepartmentInfo.Id ==department_id)
        fil.append(DepartmentInfo.Status != 10)
        department = self.session.query(DepartmentInfo).filter(*fil).all()
        return department

    async def GetDepartmentsByIds(self, department_ids):
        fil = list()
        fil.append(DepartmentInfo.Id.in_(department_ids))
        fil.append(DepartmentInfo.Status != 10)
        return await self.QueryWhere(fil)

    async def GetLeader(self,id):
        return self.session.query(DepartmentInfo).filter(DepartmentInfo.Id==id).value(DepartmentInfo.PrincipalUserId)

    async def CheckIfLeader(self, department_id, target_user_id=None):
        sys_department_info = self.Get(department_id)
        if target_user_id is None:
            return str(sys_department_info.PrincipalUserId) == str(self.UserId)
        else:
            return str(sys_department_info.PrincipalUserId) == str(target_user_id)

    async def getNextDepartments(self,id):
        return await self.QueryWhere([DepartmentInfo.ParentId==id])


    async def GetParentDepartmentInfo(self,dpInfo):
        if dpInfo.ParentId==0:
            return dpInfo
        exist=self.Get(dpInfo.ParentId)
        if exist.PrincipalUserId is not None or exist.PrincipalUserId !=0:
            return exist
        if exist.Leve==1:
            return exist
        return self.GetParentDepartmentInfo(exist)

    async def GetParentDepartmentInfoRoller(self,dpId):
        exist=self.Get(dpId)
        if exist:
            return self.GetParentDepartmentInfo(exist)
        else:
            return None

    async def getInfoByPrincipalUserId(self,userId):
        # 根据PrincipalUserId查询信息
        return await self.QueryOne([DepartmentInfo.PrincipalUserId == userId])


    async def GetUserDepartmentLeve3(self, department_id):
        fil = list()
        fil.append(DepartmentInfo.Id ==department_id)
        fil.append(DepartmentInfo.Status != 10)
        department = await self.QueryOne(fil)
        if department.Leve <= 3:
            return department
        else:
            return self.GetUserDepartmentLeve3(department.ParentId)

    async def getInfoByPrincipalUserIds(self,userId):
        # 根据PrincipalUserId查询信息
        return await self.QueryWhere([DepartmentInfo.PrincipalUserId == userId])

    async def GetPrincipalUserIds(self, right_level=None, left_level=None):
        fil = list()
        if right_level:
            fil.append(DepartmentInfo.Leve <= right_level)
        if left_level:
            fil.append(DepartmentInfo.Leve >= left_level)
        data = self.session.query(DepartmentInfo.PrincipalUserId).filter(*fil).all()
        return [item[0] for item in data]

    async def GetPrincipalUserIdsByDepType(self, dep_type: list):
        """
        获取部门、组别负责人
        """
        fil = list()
        fil.append(DepartmentInfo.DepType.in_(dep_type))
        data = self.session.query(DepartmentInfo.PrincipalUserId).filter(*fil).all()
        return [item[0] for item in data]

    async def GetUserDepartmentByLeve(self, department_id, Leve):
        fil = list()
        fil.append(DepartmentInfo.Id ==department_id)
        fil.append(DepartmentInfo.Status != 10)
        department = await self.QueryOne(fil)
        if department is None:
            return department
        if department.Leve <= Leve:
            return department
        else:
            return self.GetUserDepartmentByLeve(department.ParentId, Leve)