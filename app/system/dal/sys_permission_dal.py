# coding=UTF-8

from collections import defaultdict
from app.common.basedal import BaseDal
from sqlalchemy import or_, and_
from kxy.framework.friendly_exception import FriendlyException
from sqlalchemy.ext.asyncio import AsyncSession
from app.system.models.sys_permission import MgPermission
import re
from typing import List as TypeList

class SysPermissionDal(BaseDal[MgPermission]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__(MgPermission,db,**kwargs)

    # 获取列表
    async def List(self,search, page_index, page_size):
        fil = list()

        # fil.append(MgPermission.Status != 10)
        #if search:
        #    if re.search(r"^(\d)*$", search):
        #        fil.append(MgPermission.ID == int(search))
        #    else:
        #        search =search.strip()
        #        fil.append(MgPermission.Name.ilike("%" + search + "%"))
        return await self.paginate_query(fil, MgPermission.CreateDate.desc(), page_index, page_size)
    # 创建

    async def AddByJsonData(self, jsonData):
        entity = MgPermission()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        await self.Insert(entity)
        return entity
    async def Delete(self,id):
        exist=await self.Get(id)
        if exist!=None:
            exist.Status=10
            await self.Update(exist)
        else:
            raise FriendlyException('不存在'+str(id)+'的数据')
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
    
    async def GetMenuPermissions(self,systemcode,objectType,objectids)->TypeList[MgPermission]:
        fil = list()
        fil.append(MgPermission.SystemCode==systemcode)
        fil.append(MgPermission.ObjectType==objectType)
        fil.append(MgPermission.ObjectId.in_(objectids))
        # return await self.QueryWhere(fil)
        return await self.QueryWhere(fil,[MgPermission.MenuSchema])
    async def GetMenuPermissionsVisible(self,systemcode,objectType,objectids)->TypeList[MgPermission]:
        fil = list()
        fil.append(MgPermission.SystemCode==systemcode)
        fil.append(MgPermission.ObjectType==objectType)
        fil.append(MgPermission.ObjectId.in_(objectids))
        fil.append(MgPermission.ResourceSchema==None)
        fil.append(MgPermission.IsVisible=='1')
        return await self.QueryWhere(fil,[MgPermission.MenuSchema])
        # return await self.QueryWhere(fil)    
    async def GetUserMenuPermissions(self,systemcode,userid,roles):
        rolepermission=await self.GetMenuPermissionsVisible(systemcode,'Role',roles)
        userPermission=await self.GetMenuPermissionsVisible(systemcode,'User',[userid])
        roleKey=[item.MenuSchema for item in rolepermission]
        
        for per in userPermission:
            if per.MenuSchema not in roleKey:
                roleKey.append(per)
        return roleKey
    async def GetUserMenuAndActions(self,systemcode,objectType,objectids)->TypeList[MgPermission]:
        """获取用户菜单和菜单模块权限"""
        fil = list()
        fil.append(MgPermission.SystemCode==systemcode)
        fil.append(MgPermission.ObjectType==objectType)
        fil.append(MgPermission.ObjectId.in_(objectids))
        # fil.append(MgPermission.ResourceSchema==None)
        fil.append(MgPermission.IsEnable=='1')
        return await self.QueryWhere(fil,[MgPermission.MenuSchema,MgPermission.ResourceSchema])
        # return await self.QueryWhere(fil)

    async def GetUserPermissions(self,systemcode,userid,roles):
        rolepermission=await self.GetUserMenuAndActions(systemcode,'Role',roles)
        userPermission=await self.GetUserMenuAndActions(systemcode,'User',[userid])
        
        schemas=defaultdict(list)
        schemas={item.MenuSchema:[] for item in rolepermission}
        for item in rolepermission:
            schemas[item.MenuSchema].append(item.ResourceSchema if item.ResourceSchema else '')
        for per in userPermission:
            schemas[per.MenuSchema].append(per.ResourceSchema if per.ResourceSchema else '')
        return schemas
    
    async def GetRoleMenuPermissions(self,systemcode,roles):
        rolepermission=await self.GetMenuPermissions(systemcode,'Role',roles)
        return [item.MenuSchema for item in rolepermission]

    async def GetResourcePermissions(self,systemcode,objectType,objectids)->TypeList[MgPermission]:
        fil = list()
        fil.append(MgPermission.SystemCode==systemcode)
        fil.append(MgPermission.ObjectType==objectType)
        fil.append(MgPermission.ObjectId.in_(objectids))
        fil.append(MgPermission.IsEnable=='1')
        return await self.QueryWhere(fil,[MgPermission.MenuSchema,MgPermission.ResourceSchema])
        # return await self.QueryWhere(fil)
        
    async def GetUserResourcePermissions(self,systemcode,userid,roles):
        rolepermission=await self.GetResourcePermissions(systemcode,'Role',roles)
        userPermission=await self.GetResourcePermissions(systemcode,'User',[userid])
        roleKey=["%s$%s"%(item.MenuSchema,item.ResourceSchema) for item in rolepermission]
        for per in userPermission:
            key="%s$%s"%(per.MenuSchema,per.ResourceSchema)
            if key not in roleKey:
                roleKey.append(key)
        return roleKey
    async def GetSingleSchemaResource(self,systemcode,objectType,objectid,schemaId):
        fil = list()
        fil.append(MgPermission.SystemCode==systemcode)
        fil.append(MgPermission.ObjectType==objectType)
        fil.append(MgPermission.MenuSchema==schemaId)
        fil.append(MgPermission.ObjectId==objectid)
        return await self.QueryWhere(fil,[MgPermission.MenuSchema,MgPermission.ResourceSchema,MgPermission.IsEnable,MgPermission.IsVisible])
        # return await self.QueryWhere(fil)
    async def ChangeSchemaPower(self,systemcode,objectType,objectid,schemaId,resource,enable,visible):
        fil = list()
        fil.append(MgPermission.SystemCode==systemcode)
        fil.append(MgPermission.ObjectType==objectType)
        fil.append(MgPermission.MenuSchema==schemaId)
        fil.append(MgPermission.ObjectId==objectid)
        if resource=='/': 
            fil.append(MgPermission.ResourceSchema==None)
            resource=None
        else:
            fil.append(MgPermission.ResourceSchema==resource)

        exist=await self.QueryOne(fil)
        if exist is None:
            exist=MgPermission()
            exist.SystemCode=systemcode
            exist.ObjectType=objectType
            exist.MenuSchema=schemaId
            exist.ObjectId=objectid
            exist.ResourceSchema=resource
            if enable is not None:
                exist.IsEnable=enable
            else:
                exist.IsEnable='0'
            if visible is not None:
                exist.IsVisible=visible
            else:
                exist.IsVisible='0'
            await self.Insert(exist)
        else:
            if enable is not None:
                exist.IsEnable=enable
            if visible is not None:
                exist.IsVisible=visible
            await self.Update(exist)
        return exist
    async def GetLastUpdateMenu(self,systemcode,lastTime,endTime)->TypeList[MgPermission]:
        fil = list()
        fil.append(MgPermission.SystemCode==systemcode)
        fil.append(MgPermission.ObjectType=='Role')
        fil.append(or_(and_(MgPermission.LastModifiedDate>=lastTime,MgPermission.LastModifiedDate<endTime),and_(MgPermission.LastModifiedDate==None,MgPermission.CreateDate>=lastTime)))
        return await self.QueryWhere(fil)
        # return await self.QueryWhere(fil)

        # return await self.QueryWhere([or_(and_(MgPermission.LastModifiedDate>=lastTime,MgPermission.LastModifiedDate<endTime,MgPermission.SystemCode==systemcode),MgPermission.LastModifiedDate==None)])
    async def GetPermissionBy(self,systemcode,objectType,objectid,schemaId,ResourceSchema)->MgPermission:
        fil = list()
        fil.append(MgPermission.SystemCode==systemcode)
        fil.append(MgPermission.ObjectType==objectType)
        fil.append(MgPermission.MenuSchema==schemaId)
        fil.append(MgPermission.ResourceSchema==ResourceSchema)
        fil.append(MgPermission.ObjectId==objectid)
        return await self.QueryOne(fil)
    async def SyncJsonData(self,jsonData):
        exist=await self.GetPermissionBy(jsonData['SystemCode'],jsonData['ObjectType'],jsonData['ObjectId'],jsonData['MenuSchema'],jsonData['ResourceSchema'])
        if exist:
            exist.IsEnable=jsonData['IsEnable']
            exist.IsVisible=jsonData['IsVisible']
            await self.Update(exist)
        else:
            exist = MgPermission()
            exist.InitInsertEntityWithJson(jsonData)
            await self.Insert(exist)
    async def GetSingleModuleVisibleSchemaResource(self,systemcode,objectType,objectids,schemaId):
        fil = list()
        fil.append(MgPermission.SystemCode==systemcode)
        fil.append(MgPermission.ObjectType==objectType)
        fil.append(MgPermission.MenuSchema==schemaId)
        fil.append(MgPermission.ObjectId.in_(objectids))
        fil.append(MgPermission.IsVisible=='1')
        fil.append(MgPermission.ResourceSchema!=None)
        return await self.QueryWhere(fil,[MgPermission.ResourceSchema])
        # return await self.QueryWhere(fil)
    def Distinct(self,entitys,exist):        
        for entity in entitys:
            key=entity.ResourceSchema
            if key is None:
                key='/'                
            if key not in exist:
                exist.append(key)

    async def GetUserSingleModuleResource(self,systemcode,moduleId,user_id,userRoleIds):
        user_rs=await self.GetSingleModuleVisibleSchemaResource(systemcode,'User',[user_id],moduleId)
        role_rs=await self.GetSingleModuleVisibleSchemaResource(systemcode,'Role',userRoleIds,moduleId)
        exist=[]
        self.Distinct(user_rs,exist)
        self.Distinct(role_rs,exist)
        return exist
    
    async def GetSingleEnableSchemaResource(self,systemcode,objectType,objectids,schemaId):
        fil = list()
        fil.append(MgPermission.SystemCode==systemcode)
        fil.append(MgPermission.ObjectType==objectType)
        fil.append(MgPermission.MenuSchema==schemaId)
        fil.append(MgPermission.ObjectId.in_(objectids))
        fil.append(MgPermission.IsEnable=='1')
        fil.append(MgPermission.ResourceSchema!=None)
        return await self.QueryWhere(fil,fields=[MgPermission.ResourceSchema])
        # return await self.QueryWhere(fil)
        
    async def GetUserModuleEnableResouce(self,systecode,user_id,userRoleIds,Module):
        user_rs=await self.GetSingleEnableSchemaResource(systecode,'User',[user_id],Module)
        role_rs=await self.GetSingleEnableSchemaResource(systecode,'Role',userRoleIds,Module)
        role_rs=[rs.ResourceSchema for rs in role_rs]

        for rs in user_rs:
            if rs.ResourceSchema not in role_rs:
                role_rs.append(rs.ResourceSchema)
        return role_rs
    async def DeleteBy(self,SystemCode,Schema):
        await self.TrueDelWhere([MgPermission.SystemCode==SystemCode,MgPermission.MenuSchema==Schema])