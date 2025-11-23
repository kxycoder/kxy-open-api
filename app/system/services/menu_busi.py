
import asyncio
import json
import requests,time,json
from app.common.menu_tree import MenuTree
from app.global_var import Gkey, Keys
from app.system.models.sys_menu import MgMenu
from app.system.dal.sys_users_dal import SysUsersDal
from app.system.dal.sys_menu_dal import SysMenuDal
from app.system.dal.sys_permission_dal import SysPermissionDal
from app.system.dal.sys_role_user_dal import SysRoleUserDal
from app.system.dal.sysnc_record_dal import SysncRecordDal
from app.system.dal.sys_public_dictionary_dal import SysPublicDictionaryDal
from app.system.dal.sys_role_dal import SysRoleDal
from app.system.dal.sys_resource_dal import SysResourceDal
from app.system.dal.sys_system_dal import SysSystemDal
# from app.common.util import MenuTree
from kxy.framework.friendly_exception import FriendlyException
from app.config import config
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)
# from app.common.sso_api import SyncDataToRemote
from datetime import datetime,timedelta
import traceback
from app.database import get_redis_client
from app.system.services.base_service import BaseService
from kxy.framework.util import SUtil


sync_types={'systemcode':SysSystemDal,
            'menu':SysMenuDal,
            'resource':SysResourceDal,
            'role':SysRoleDal,
            'permissions':SysPermissionDal,
            'dictionary':SysPublicDictionaryDal
            }      
        
class MenuBusi(BaseService):
    def __init__(self,session,**kwargs):        
        super().__init__(session,**kwargs)
        self.cache=get_redis_client()
    async def GetBaseUserMenus(self,systemcode,isdisplay):
        try:
            menuDal=SysMenuDal(self.session)
            perDal=SysPermissionDal(self.session)        
            userRoleIds=await self.GetUserRolesIdCache(systemcode,self.user_id)
            menuSchemas=await perDal.GetUserMenuPermissions(systemcode,self.user_id,userRoleIds)
            menus=await menuDal.GetMeus(systemcode,menuSchemas,isdisplay)
            return menus
        except Exception as ex:
            logger.error(traceback.format_exc(limit=5))
            raise ex
        
    async def GetUserMenus(self,systemcode,isdisplay):
        menus=await self.GetBaseUserMenus(systemcode,isdisplay)
        return MenuTree.ToTreeLower(menus)
    
    async def GetUserMenuAndActions(self,systemcode,isdisplay):
        try:
            menuDal=SysMenuDal(self.session)
            perDal=SysPermissionDal(self.session)        
            userRoleIds=await self.GetUserRolesIdCache(systemcode,self.user_id)
            userRoleNames = await self.GetUserRolesNameCache(systemcode,self.user_id)
            menuSchemas=await perDal.GetUserPermissions(systemcode,self.user_id,userRoleIds)
            menuSchamaIds = list(menuSchemas.keys())
            menus = await menuDal.GetMeus(systemcode,menuSchamaIds,isdisplay)
            for menu in menus:
                menu.Actions = list(set(menuSchemas[menu.Schema]))
            result ={
                'menus': MenuTree.ToTreeLower(menus),
                'permissions':menuSchamaIds,
                'roles':userRoleNames
                }
            return result
        except Exception as ex:
            logger.error(traceback.format_exc(limit=5))
            raise ex
    async def GetUserPermissions(self,systemcode):        
        perDal=SysPermissionDal(self.session)
        userRoleIds=await self.GetUserRolesId(systemcode,self.user_id)
        menuSchemas=await perDal.GetUserPermissions(systemcode,self.user_id,userRoleIds)
        return menuSchemas

    async def GetUserMenusAnt(self,systemcode,isdisplay):
        menus=await self.GetBaseUserMenus(systemcode,isdisplay)
        return MenuTree.ToTreeLowerAnt(menus)
    
    async def ClearSystemCodeCache(self,systemcode):
        key1=f'{systemcode}:*'
        asyncio.create_task(self.ClearBatchKey(key1))
    
    async def GetUserAllMenus(self,systemcode,userid):
        menuDal=SysMenuDal(self.session)
        perDal=SysPermissionDal(self.session)
        userRoleIds=await self.GetUserRolesId(systemcode,userid)
        menuSchemas=await perDal.GetUserMenuPermissions(systemcode,userid,userRoleIds)
        menus=await menuDal.GetMeus(systemcode,menuSchemas)
        return MenuTree.ToTree(menus)
    async def GetRoleAllMenus(self,systemcode,roleid):
        menuDal=SysMenuDal(self.session)
        perDal=SysPermissionDal(self.session)        
        menuSchemas=await perDal.GetRoleMenuPermissions(systemcode,[roleid])
        menus=await menuDal.GetMeus(systemcode,menuSchemas)
        return MenuTree.ToTree(menus)

    async def GetSystemAllMenu(self,systemcode,search = ''):
        menuDal=SysMenuDal(self.session)
        menus=await menuDal.GetSystemMenus(systemcode)
        return MenuTree.ToTree(menus,'0',search)
        
    async def GetSystemRoles(self,systemcode,userid):
        dal=SysRoleDal(self.session)
        roles=await dal.GetSystemRoles(systemcode)
        return roles

    async def GetUserRoles(self,systemcode,userid):
        roleDal=SysRoleUserDal(self.session)
        roles=await self.GetSystemRoles(systemcode,userid)
        systemRoles=[role.Id for role in roles]
        userRoles=await roleDal.GetUserRoles(userid,systemRoles)
        return userRoles

    async def GetUserRolesId(self,systemcode,userid):
        userRoles=await self.GetUserRoles(systemcode,userid)
        return [role.RoleId for role in userRoles]
    async def GetUserRolesIdCache(self,systemcode,userid,clear=False):
        key = Gkey(Keys.USER_ROLES_ID,systemcode,userid)
        roles = await self.cache.get(key)
        if config.ENV_NAME=='dev' or not roles or clear:
            userRoles=await self.GetUserRoles(systemcode,userid)
            if not userRoles:
                roles = []
            else:
                roles = [role.RoleId for role in userRoles]
            await self.cache.set(key, json.dumps(roles),2280)
        else:
            roles = json.loads(roles)
        return roles
    async def GetUserRolesNameCache(self,systemcode,userid,clear=False):
        key = Gkey(Keys.USER_ROLES,systemcode,userid)
        roles = await self.cache.get(key)
        if not roles or clear:
            userRoles=await self.GetUserRoles(systemcode,userid)
            if not userRoles:
                roles = []
            else:
                roleIds = [role.RoleId for role in userRoles]
                roles =await SysRoleDal(self.session).GetRolesByIds(roleIds)
            await self.cache.set(key, json.dumps(roles),2280)
        else:
            roles = json.loads(roles)
        return roles
    async def GetUserRoleNames(self,systemcode,userid):
        key = Gkey(Keys.USER_ROLES,systemcode,userid)
        roles=await self.cache.get(key)
        if roles is not None:
            return json.loads(roles)

        roleDal=SysRoleUserDal(self.session)
        roles=await self.GetSystemRoles(systemcode,userid)
        systemRolesIds=[role.Id for role in roles]
        userRoles=await roleDal.GetUserRoles(userid,systemRolesIds)
        userRoleIds=[role.RoleId for role in userRoles]
        roleNames=[]
        for role in roles:
            if role.Id in userRoleIds:
                roleNames.append({"id":role.Id,"roleName":role.Name})
        if len(roleNames)==0:
            dal=SysRoleDal(self.session)
            guestRoleId=await dal.AddGuestRole(systemcode)
            guest=await roleDal.AddGuestRole(userid,guestRoleId)
            return [{'id':guest.Id,'roleName':'Guest'}]
        await self.cache.set(key,json.dumps(roleNames,ensure_ascii=False),3600)
        return roleNames
    async def AddSystemCode(self,jsonData):
        dal=SysSystemDal(self.session)
        entity=await dal.AddByJsonData(jsonData)
        roleDal=SysRoleDal(self.session)
        await roleDal.AddGuestRole(entity.SystemCode)
        return entity

    async def CheckPermission(self,systemcode,userId,permissions):
        items=permissions.split('$')
        moduleName=items[0]
        source=items[1]
        key=Gkey(Keys.USER_PERMISSION,systemcode,userId,moduleName,source)
        per=await self.cache.get(key)
        if per is not None:
            return per.decode('utf-8')=='1'


        userRoleIds=await self.GetUserRolesId(systemcode,userId)
        perDal=SysPermissionDal(self.session)
        userPermissions= await perDal.GetUserResourcePermissions(systemcode,userId,userRoleIds)
        if permissions in userPermissions:
            await self.cache.set(key,1,3600)
            return True
        else:
            if config.AutoAddModel==True:
                menuDal=SysMenuDal(self.session)
                menu=await menuDal.GetMenu(systemcode,moduleName)
                if menu:
                    sourceDal=SysResourceDal(self.session)
                    if not await sourceDal.Exist(menu.Id,source):
                        await sourceDal.Add(menu.Id,source)
                        adminRole=await SysRoleDal(self.session).ExistRole(menu.SystemCode,'superadmin')
                        if adminRole:
                            await self.ChangeRoleResourcePower(menu.SystemCode,adminRole.Id,menu.Schema,{'name':source,"IsEnable":"1"})
            await self.cache.set(key,0,3600)
            return False

    async def GetUserVisibleCacheKey(self,systemcode,module,userid):
        return 'opt_sso:vis:%s:%s:%s'%(systemcode,module,userid)
    
    async def GetModuleVisible(self,systemcode,userId,module):
        key=await self.GetUserVisibleCacheKey(systemcode,module,userId)
        result=await self.cache.get(key)
        if result is None:
            perDal=SysPermissionDal(self.session)
            userRoleIds=await self.GetUserRolesId(systemcode,userId)

            perDal=SysPermissionDal(self.session)
            resource= await perDal.GetUserSingleModuleResource(systemcode,module,userId,userRoleIds)

            await self.cache.set(key,json.dumps(resource),86400)
            return resource
        else:
            return json.loads(result)

    async def SaveMenus(self,menus,parentId=0):
        index=0
        menuDal=SysMenuDal(self.session)
        for menu in menus:
            id=menu['Id']
            exist=await menuDal.Get(id)
            exist.Sort=index
            exist.ParentId=parentId
            await menuDal.Update(exist)
            Children=menu['Children']
            if len(Children)>0:
                await self.SaveMenus(Children,id)
            index+=1
    async def GetSchemaResource(self,systemcode,objecttype,objectid,schemaId,MenuId):
        perDal=SysPermissionDal(self.session)
        userSchemaResources= await perDal.GetSingleSchemaResource(systemcode,objecttype,objectid,schemaId)
        userResources={}
        for userresource in userSchemaResources:
            if userresource.ResourceSchema is None:
                userResources['/']=userresource
            userResources[userresource.ResourceSchema]=userresource

        resourceDal=SysResourceDal(self.session)
        resourceEntitys=await resourceDal.GetSchemaResource(MenuId)
        resources=[resource.to_basic_dict() for resource in resourceEntitys]
        resources.insert(0,{
            'Description': '',
            'Name': "",
            'Schema': "/",
        })
        for resource in resources:
            MenuSchema=resource['Schema']
            exist=userResources.get(MenuSchema, None)
            if exist!=None:
                resource['IsEnable']=exist.IsEnable
                resource['IsVisible']=exist.IsVisible      
            else:
                resource['IsEnable']='0'
                resource['IsVisible']='0'

        
        return resources
    async def GetUserResource(self,systemcode,userid,schemaId,MenuId):        
        return await self.GetSchemaResource(systemcode,'User',userid,schemaId,MenuId)
    async def GetRoleResource(self,systemcode,roleId,schemaId,MenuId):
        return await self.GetSchemaResource(systemcode,'Role',roleId,schemaId,MenuId)
    async def ChangeSchemaPower(self,systemcode,objecttype,objectid,schemaId,resource):
        perDal=SysPermissionDal(self.session)
        name=resource.get('name',None)
        IsEnable=resource.get('IsEnable',None)
        IsVisible=resource.get('IsVisible',None)
        # if IsVisible=='1' and name=='/':
        #     menuDal=MgMenuDal(self.session)
        #     menu=menuDal.GetMenu(systemcode,schemaId)
        #     if menu.IsDisplay=='0': 
        #         raise FriendlyException('菜单本身配置为不展示，此处配置展示无用')
        await perDal.ChangeSchemaPower(systemcode,objecttype,objectid,schemaId,name,IsEnable,IsVisible)
    async def ClearRoleResourceCache(self,systemcode,schema,source):
        # key='opt_sso:per:%s:%s$%s:*' % (systemcode,schema,source) 
        key = Gkey(Keys.USER_PERMISSION,systemcode,'*',schema,source)
        await self.ClearBatchKey(key)
        # key='opt_sso:vis:%s:%s:*'%(systemcode,schema)
        # await self.ClearBatchKey(key)

    async def ClearBatchKey(self,key):        
        keys=await self.cache.keys(pattern=key)
        if len(keys) > 0:
            await self.cache.delete(*keys)

    async def ClearUserSingleCache(self,systemcode,schema,source,userid):
        key='opt_sso:per:%s:%s$%s:%s' % (systemcode,schema,source,userid) 
        key = Gkey(Keys.USER_PERMISSION,systemcode,userid,schema,source)
        await self.cache.delete(key)
        # key=await self.GetUserVisibleCacheKey(systemcode,schema,userid)
        # await self.cache.delete(key)

    async def ClearUserAllCache(self,systemcode,userid):
        key = Gkey(Keys.USER_ROLES,systemcode,userid)
        await self.cache.delete(key)

        # key='opt_sso:per:%s:*:%s' % (systemcode,userid) 
        key = Gkey(Keys.USER_PERMISSION,systemcode,userid,'*','*')
        await self.ClearBatchKey(key)
        
        # key=await self.GetUserSystemCodeCacheKey(systemcode,userid)
        # await self.cache.delete(key)        
        key='opt_sso:user:enablesource:%s:%s:%s'%(systemcode,'*',userid)
        await self.ClearBatchKey(key)

    async def ClearAllUserSystemCache(self,systemcode):
        key='opt_sso:user:enablesource:%s:*'%(systemcode)
        await self.ClearBatchKey(key)

    async def ChangeUserResourcePower(self,systemcode,userid,schemaId,resource):
        await self.ChangeSchemaPower(systemcode,'User',userid,schemaId,resource)
        await self.ClearUserSingleCache(systemcode,schemaId,resource.get('name',None),userid)

    async def ChangeRoleResourcePower(self,systemcode,roleid,schemaId,resource):
        await self.ChangeSchemaPower(systemcode,'Role',roleid,schemaId,resource)
        await self.ClearRoleResourceCache(systemcode,schemaId,resource.get('name',None))
        await self.ClearAllUserSystemCache(systemcode)

    async def SyncToRemote(self,systemcode,name,datas):
        if len(datas)>0:
            rqdata={
                "systemcode":systemcode,
                "datatype":name,
                "datas":[data.to_basic_dict() for data in datas]
            }
            dal = SysPublicDictionaryDal(self.session)
            remoteUrls = await dal.GetDictionary(systemcode,'RemoteSSOUrl')
            if not remoteUrls:
                return
            for remoteUrl in remoteUrls:
                url=remoteUrl.Value
                if 'X-Token' not in url:
                    raise FriendlyException('同步到远程的链接中没有配置X-Token')
                if url:
                    realUrl= url.split('X-Token')
                    
                    response = requests.post(url,json=rqdata,timeout=10)
                    if response.status_code==200:
                        rqresult=response.json()
                        if rqresult.get('success',False):
                            continue
                        raise FriendlyException('同步%s失败%s,json:%s'%(name,rqresult.get('error'),rqdata))

    async def SyncMenu(self,systemcode):
        result=[]
        beginDate=datetime.now()+timedelta(days=-365)
        syncDal=SysncRecordDal(self.session)
        last_sync_record=await syncDal.GetLastSyncDate('menu',systemcode)
        if last_sync_record is not None:
            beginDate=last_sync_record.SyncDate

        sync_record=await syncDal.CreateSyncRecord('menu',systemcode)
        nowDate=sync_record.SyncDate

        systemDal=SysSystemDal(self.session)
        datas=await systemDal.GetLastUpdateMenu(beginDate,nowDate)
        await self.SyncToRemote(systemcode,'systemcode',datas)
        result.append('systemcode成功同步%s条数据'%len(datas))

        menuDal=SysMenuDal(self.session)
        menus=await menuDal.GetLastUpdateMenu(systemcode,beginDate,nowDate)
        await self.SyncToRemote(systemcode,'menu',menus)
        result.append('menu成功同步%s条数据'%len(menus))

        resourceDal=SysResourceDal(self.session)
        allMenus=await menuDal.GetSystemMenus(systemcode)
        allMenusIds=[item.Id for item in allMenus]
        # for menu in menus:
        resources=await resourceDal.GetLastUpdateMenu(allMenusIds,beginDate,nowDate)
        if len(resources)>0:
            await self.SyncToRemote(systemcode,'resource',resources)
            result.append('resource成功同步%s条数据'%len(resources))

        roleDal=SysRoleDal(self.session)
        roles=await roleDal.GetLastUpdateMenu(systemcode,beginDate,nowDate)
        await self.SyncToRemote(systemcode,'role',roles)
        result.append('role成功同步%s条数据'%len(roles))
        
        permissionDal=SysPermissionDal(self.session)
        permissions=await permissionDal.GetLastUpdateMenu(systemcode,beginDate,nowDate)
        await self.SyncToRemote(systemcode,'permissions',permissions)
        result.append('permissions成功同步%s条数据'%len(permissions))

        dicDal=SysPublicDictionaryDal(self.session)
        dics=await dicDal.GetLastUpdateMenu(systemcode,beginDate,nowDate)
        await self.SyncToRemote(systemcode,'dictionary',dics)
        result.append('dictionary成功同步%s条数据'%len(dics))

        # for name,synctype in sync_types.items():
        #     dal=synctype(self.user_id,self.session)
        #     datas=await dal.GetLastUpdateMenu(systemcode,beginDate,nowDate)
        #     if len(datas)>0:
        #         rqdata={
        #             "datatype":name,
        #             "datas":MenuTree.formatListData(datas)
        #         }
        #         rqresult=SyncDataToRemote(rqdata)
        #         if rqresult['status']==False:
        #             raise FriendlyException('同步%s失败%s'%(name,rqresult.get('error')))
        sync_record.Status=5
        await syncDal.Update(sync_record)
        return result
    async def SynMenuRevice(self,jsonData):
        """{
            "datatype":"menu",
            "datas":[]
        }"""
        datatype=jsonData.get('datatype')
        daltype=sync_types.get(datatype,None)
        if daltype is None:
            raise FriendlyException('没有找到'+datatype)
        dal=daltype(self.session)
        for data in jsonData.get('datas'):
            await dal.SyncJsonData(data)
    async def GetUserSystemCodeCacheKey(self,systecode,module,userid):            
        return 'opt_sso:user:enablesource:%s:%s:%s'%(systecode,module,userid)

    async def GetUserEnabledResource(self,systecode,user_id,Module):        
        perDal=SysPermissionDal(self.session)
        userRoleIds=await self.GetUserRolesId(systecode,user_id)
        menuSchemas=await perDal.GetUserModuleEnableResouce(systecode,user_id,userRoleIds,Module)
        return menuSchemas

    async def GetEnabledResource(self,systecode,user_id,Module):
        # menuDal=MgMenuDal(self.session)
        key=await self.GetUserSystemCodeCacheKey(systecode,Module,user_id)
        cache=await self.cache.get(key)
        menuSchemas=[]
        if cache is not None:
            menuSchemas=await self.GetUserEnabledResource(systecode,user_id,Module)
            await self.cache.set(key,json.dumps(menuSchemas),86400)
        else:
            menuSchemas=json.loads(cache)
        return menuSchemas
        
    async def GetUserEnableSysmteCode(self,userid):
        menuSchemas=await self.GetEnabledResource(config.SystemCode,userid,'systemcode')
        systemDal=SysSystemDal(self.session)
        results=await systemDal.GetListBy(menuSchemas)
        return results
    
    async def InitMenu(self,datas):
        menuId = datas.get('menuId')
        dal=SysMenuDal(self.session)
        if menuId:
            menuInfo = await dal.Get(menuId)
            return await self.InitMenuPermission(menuInfo)
        systemcode=datas.get('systemcode')
        if not systemcode:
            raise FriendlyException('必须传入systemcode系统标识')
        schema=datas.get('schema')
        if not schema:
            raise FriendlyException('必须传入schema权限标识')
        menuName=datas.get('menuName')
        if not menuName:
            raise FriendlyException('必须传入menuName菜单名称')
        parent_id=datas.get('parent_id',0)
        systemDal=SysSystemDal(self.session)
        code=await systemDal.GetBySystemCode(systemcode)
        if not code :
            raise FriendlyException(f'systemcode:{systemcode}不存在')
        
        exist:MgMenu=await dal.GetMenu(systemcode,schema)
        if not exist:
            payload={
            "SystemCode": systemcode,
            "ParentId": parent_id,
            "Name": menuName,
            "Description": menuName,
            "Schema": schema,
            "RouteUrl": f"/{schema}",
            "NavigateUrl": f"/{schema}",
            "Target": "",
            "IconUrl": "",
            "Sort": "0",
            "IsDisplay": "0"
            }
            exist=await dal.AddByJsonData(payload)
        await self.InitMenuPermission(exist)
    async def InitMenuPermission(self,menuInfo:MgMenu):
        resource_dal=SysResourceDal(self.session)
        defaultSources=[
            {'key':'/','des': '/'},
            {'key':'add','des': '添加'},
            {'key':'delete','des': '删除'},
            {'key':'update','des': '编辑'},
            {'key':'get','des': '获取单条数据详情'},
            {'key':'list','des': '获取数据列表'},
            {'key':'export_excel','des': '导出数据'},
        ]
        roleDal=SysRoleDal(self.session)
        adminRole=await roleDal.ExistRole(menuInfo.SystemCode,'superadmin')
        for resource in defaultSources:
            try:
                source=await resource_dal.Add(menuInfo.Id, resource['key'], resource['des'])
                if adminRole:
                    await self.ChangeRoleResourcePower(menuInfo.SystemCode,adminRole.Id,menuInfo.Schema,{'name':resource['key'],"IsEnable":"1"})
            except:
                logger.error(f"初始化菜单资源失败{resource['key']}")
    async def InitSuperAdminMenu(self,systemCode):
        userDal = SysUsersDal(self.session)
        menus =await SysMenuDal(self.session).GetAllMenus(systemCode)
        adminRole =await SysRoleDal(self.session).GetRoleByName(systemCode,'superadmin')
        for menuInfo in menus:
            await self.ChangeRoleResourcePower(menuInfo.SystemCode,adminRole.Id,menuInfo.Schema,{'name':'/',"IsEnable":"1"})
        # superUser = await SysRoleUserDal(self.session).GetUserByRoleId(systemCode,superRole.Id)
        # superAdmin = await userDal.GetByUserName('superadmin')
        # if not superAdmin:
        #     await userDal.AddNewUser('superadmin','123456','123456789')
    async def InitMenuPublic(self,datas):
        url=datas.get('ssourl')
        if not url:
            raise FriendlyException('请输入ssourl')
        code_sso_token=datas.get('code_sso_token')
        if not code_sso_token:
            raise FriendlyException('请输入code_sso_token')
        headers = {
            'Cookie': "opt.authorize="+code_sso_token,
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
        }

        response = requests.request("POST", url,headers=headers,json=datas)
        
        return response.json()
    async def DeleteMenu(self,id):
        menuDal = SysMenuDal(self.session)
        perDal = SysPermissionDal(self.session)
        sourceDal = SysResourceDal(self.session)
        allMenus =await menuDal.GetSelfAndChildrens(id)
        if not allMenus:
            raise FriendlyException('没有找到菜单')
        async with menuDal:
            for menu in allMenus:
                await perDal.DeleteBy(menu.SystemCode,menu.Schema)
                await sourceDal.DeleteByMenuId(menu.Id)
                await menuDal.TrueDel(menu.Id)
            # MgResourceDal(self.session).GetMenuResource(id)
            
            await menuDal.Delete(id)
    async def SyncUIMenu(self,jsonData):
        systemcode = jsonData.get('SystemCode')
        routes = jsonData.get('Routes')
        await self._genUiMenu(systemcode,routes,'0')
    async def _genUiMenu(self,systemcode,routes,parentId):
        menus = []
        sortIndex = 0
        menuDal = SysMenuDal(self.session)
        for route in routes:
            sortIndex +=1
            hidden = route.get('hidden',False)
            if hidden:
                continue
            Name = route.get('name')
            if not Name:
                continue
            menu =await menuDal.GetMenuByName(systemcode,Name)
            if not menu:
                menu = MgMenu()
                menu.IsDisplay = 1
                menu.SystemCode = systemcode
                menu.Name = route.get('name')
                menu.Schema = Name
                menu.Sort = sortIndex
                menu.RouteUrl = route.get('path','')
                menu.NavigateUrl = route.get('path','')
                menu.IconUrl = route.get('meta',{}).get('icon')
                menu.Description = route.get('description',Name)
                menu.ParentId = parentId
                await menuDal.Insert(menu)
            # else:
            #     icon = route.get('meta',{}).get('icon')
            #     if icon:
            #         menu.IconUrl = icon
            #     menu.Description = route.get('description',Name)
            #     await menuDal.Update(menu)
            children = route.get('children',[])
            if children:
                await self._genUiMenu(systemcode,children,menu.Id)
            