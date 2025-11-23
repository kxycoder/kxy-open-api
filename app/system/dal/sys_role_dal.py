# coding=UTF-8

from app.common.basedal import BaseDal
from kxy.framework.friendly_exception import FriendlyException
from sqlalchemy.ext.asyncio import AsyncSession
from app.system.models.sys_role import MgRole
from app.config import config
from sqlalchemy import and_,or_
from typing import List as TypeList
import re

class SysRoleDal(BaseDal[MgRole]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__(MgRole,db,**kwargs)

    # 获取列表
    async def List(self,search,roles,systemcode, page_index, page_size):
        fil = list()

        # fil.append(MgRole.Status != 10)
        if search:
           if re.search(r"^(\d)*$", search):
               fil.append(MgRole.Id == int(search))
           else:
               search =search.strip()
               fil.append(MgRole.Name.ilike("%" + search + "%"))
        if systemcode:
            fil.append(MgRole.SystemCode==systemcode)
        if 'superadmin' not in roles:
            fil.append(MgRole.Name.not_in(['superadmin','admin']))

        return await self.paginate_query(fil, MgRole.CreateDate.desc(), page_index, page_size)
    
    
    # Ant列表查询
    async def ListAnt(self,search,page_index, page_size):
        fil = list()
        # fil.append(MgRole.Status != 10)
        if search.get('Id'):
            fil.append(MgRole.Id==int(search.get('Id')))
        if search.get('Name'):
            fil.append(MgRole.Name.ilike(f"%{search.get('Name')}%"))
        # if search.get('SystemCode'):
        fil.append(MgRole.SystemCode==config.SystemCode)
        f=self.session.query(MgRole).filter(*fil)
        total=f.count()
        datas=f.order_by(MgRole.CreateDate.desc()).offset((page_index-1)*page_size).limit(page_size)
        return total,datas

    async def AddByJsonData(self, jsonData):
        entity = MgRole()
        entity.InitInsertEntityWithJson(jsonData)    
        # entity.SystemCode=config.SystemCode
        entity.Status = 1
        await self.Insert(entity)
        return entity
    async def Delete(self,id):
        exist = await self.GetExist(id)
        if exist.Name in ['admin','superadmin','backuser']:
            raise FriendlyException('系统内置角色不能删除')
        await self.TrueDel(id)
    async def deletebatch(self,ids):
        self.TrueDelBatch(ids)
        
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
    async def GetSystemRoles(self,systemcode):
        return await self.QueryWhere([MgRole.SystemCode==systemcode])
    async def ExistRole(self,systemcode,role)->MgRole:
        return await self.QueryOne([MgRole.SystemCode==systemcode,MgRole.Name==role])
    async def AddGuestRole(self,systemcode):
        exist=await self.ExistRole(systemcode,'Guest')
        if not exist:
            exist = MgRole()
            exist.Name='Guest'
            exist.Description='访客'
            exist.SystemCode=systemcode
            await self.Insert(exist)
        return exist.Id
    async def GetLastUpdateMenu(self,systemcode,lastTime,endTime):
        fil = list()
        fil.append(MgRole.SystemCode==systemcode)
        fil.append(or_(and_(MgRole.LastModifiedDate>=lastTime,MgRole.LastModifiedDate<endTime),and_(MgRole.LastModifiedDate==None,MgRole.CreateDate>=lastTime)))
        return await self.QueryWhere(fil)
    async def GetRolesByIds(self,ids)->TypeList[str]:
        results = await self.QueryWhere([MgRole.Id.in_(ids)],[MgRole.Name])
        return [x.Name for x in results]
    async def SyncJsonData(self,jsonData):     
        exist=await self.ExistRole(jsonData['SystemCode'],jsonData['Name'])
        if exist:
            exist.Description=jsonData['Description']
            await self.Update(exist)
        else:
            exist = MgRole()
            exist.InitInsertEntityWithJson(jsonData)            
            await self.Insert(exist)
    async def GetRoleByName(self,systemcode,roleName):
        return await self.QueryOne([MgRole.SystemCode==systemcode,MgRole.Name==roleName])