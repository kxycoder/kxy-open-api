# coding=UTF-8

from app.common.basedal import BaseDal
from kxy.framework.friendly_exception import FriendlyException
from sqlalchemy.ext.asyncio import AsyncSession
from app.system.models.sys_role_user import MgRoleUser
from app.system.models.sys_role import MgRole
import re

class SysRoleUserDal(BaseDal[MgRoleUser]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__(MgRoleUser,db,**kwargs)

    # 获取列表
    async def List(self,search,userid, systemcode,page_index, page_size):
        fil = list()

        # fil.append(MgRoleUser.Status != 10)
        if search:
           if re.search(r"^(\d)*$", search):
               fil.append(MgRoleUser.ID == int(search))
           else:
               search =search.strip()
               fil.append(MgRoleUser.Name.ilike("%" + search + "%"))
        if systemcode:
            fil.append(MgRole.SystemCode==systemcode)
        if userid:
            fil.append(MgRoleUser.UserId==userid)
        fields = [MgRoleUser.UserId,MgRoleUser.RoleId,MgRoleUser.Id,MgRole.SystemCode,MgRole.Name,MgRole.Description] 
        return await self.paginate_fields_query(fields,fil,MgRoleUser.CreateDate.desc(),page_index, page_size)    

    async def AddByJsonData(self, jsonData):
        entity = MgRoleUser()
        entity.InitInsertEntityWithJson(jsonData)    
        await self.Insert(entity)
        return entity
    async def Delete(self,id):
        await self.TrueDel(id)
    async def UpdateByJsonData(self,jsonData):
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity=await self.Get(id)
        if not entity:
            raise FriendlyException('不存在'+str(id)+"的数据")
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity
    async def GetUserRoles(self,userid,systemcodeRoles):
        return await self.QueryWhere([MgRoleUser.UserId == userid,MgRoleUser.RoleId.in_(systemcodeRoles)])
    async def AddByFields(self,RoleId,userid):
        entity = MgRoleUser()
        entity.RoleId=RoleId
        entity.UserId=userid
        await self.Insert(entity)
        return entity    
    async def AddGuestRole(self,userid,roleid):
        return self.AddByFields(roleid,userid)