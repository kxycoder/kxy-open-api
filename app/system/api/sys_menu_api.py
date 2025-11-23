# !/usr/bin/python
# -*- coding:utf-8 -*-
import re
import traceback
from fastapi import APIRouter, Depends, Request

from app.system.services.user_service import UserService
router = APIRouter()

from app.common.result import Result
from kxy.framework.friendly_exception import FriendlyException
from app.system.dal.sys_menu_dal import SysMenuDal
from app.common.filter import auth_module, get_admin_user
from app.system.services.menu_busi import MenuBusi

@router.get("/userMenus")
async def userMenus(request: Request,current_user: str = Depends(get_admin_user)):
    systemCode = request.query_params.get("systemCode", '')
    dal = MenuBusi(request.state.db)
    data = await dal.GetUserMenus(systemCode,'1')
    return Result.success(data)    

@router.get("/permissions_and_actions")
async def permissions_and_actions(request: Request,current_user: str = Depends(get_admin_user)):

    systemCode = request.query_params.get("systemCode", '')
    dal = MenuBusi(request.state.db)
    data = await dal.GetUserPermissions(systemCode)
    return Result.success(data)    
@router.get("/userMenusAnt")
async def userMenusAnt(request: Request,current_user: str = Depends(get_admin_user)):

    systemCode = request.query_params.get("systemCode", '')
    dal = MenuBusi(request.state.db)
    data = await dal.GetUserMenusAnt(systemCode,'1')
    return Result.success(data)
@router.get("/sys_menu/get_user_all_menus")
@auth_module(module_name="sys_menu", resource="get_user_all_menus")
async def get_user_all_menus(request: Request,current_user: str = Depends(get_admin_user)):
    systemCode = request.query_params.get("systemcode", '')
    userid= request.query_params.get("userid",None)
    dal = MenuBusi(request.state.db)
    data = await dal.GetUserAllMenus(systemCode,userid)
    return Result.success(data)
@router.get("/sys_menu/get_role_all_menus")
@auth_module(module_name="sys_menu", resource="get_role_all_menus")
async def get_role_all_menus(request: Request,current_user: str = Depends(get_admin_user)):
    systemCode = request.query_params.get("systemcode", '')
    roleid= request.query_params.get("roleid",None)

    dal = MenuBusi(request.state.db)
    data = await dal.GetRoleAllMenus(systemCode,roleid)
    return Result.success(data)
@router.get("/getUserRoles")
async def getUserRoles(request: Request,current_user: str = Depends(get_admin_user)):    
    systemCode = request.query_params.get("systemCode", None)
    userId=request.query_params.get("userId", None)
    if systemCode is None or systemCode == "":
        raise FriendlyException('请传入systemCode')
    if userId is None:
        raise FriendlyException('请传入userId')

    dal = MenuBusi(request.state.db)
    data =await dal.GetUserRoleNames(systemCode,userId)
    return Result.success(data)
@router.get("/checkPermission")
async def checkPermission(request: Request,current_user: str = Depends(get_admin_user)):    
    systemCode = request.query_params.get("systemCode", None)
    permissions=request.query_params.get("permissions",None)
    userId=request.query_params.get("userId", None)

    dal = MenuBusi(request.state.db)
    data =await dal.CheckPermission(systemCode,userId,permissions)
    if data==True:
        return "true"
    else:
        return "false"

@router.get("/sys_menu/list")
@auth_module(module_name="sys_menu", resource="list")
async def mg_menu_list(request: Request,current_user: str = Depends(get_admin_user)):
    systemCode = request.query_params.get("systemCode", None)
    search = request.query_params.get("search", '')
    if systemCode is None:
        raise FriendlyException('请传入systemCode')
    dal = MenuBusi(request.state.db)
    data = await dal.GetSystemAllMenu(systemCode,search)
    return Result.success(data)
@router.post("/sys_menu/save_menus")
@auth_module(module_name="sys_menu", resource="save_menus")
async def save_menus(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MenuBusi(request.state.db)
    jsonData = await request.json()
    data =await dal.SaveMenus(jsonData)
    return Result.success('保存成功')
@router.post("/sys_menu/add")
@auth_module(module_name="sys_menu", resource="add")
async def mg_menu_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysMenuDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)
    return Result.success(data)
@router.post("/sys_menu/update")
@auth_module(module_name="sys_menu", resource="update")
async def mg_menu_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysMenuDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)
    return Result.success(data)
@router.get("/sys_menu/delete/{id}")
@auth_module(module_name="sys_menu", resource="delete")
async def mg_menu_delete(id,request: Request,current_user: str = Depends(get_admin_user)):    
    dal = MenuBusi(request.state.db)
    data = await dal.DeleteMenu(id)
    return Result.success("删除成功")

@router.get("/sys_menu/get/{id}")
@auth_module(module_name="sys_menu", resource="get")
async def mg_menu_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysMenuDal(request.state.db)
    data = await dal.Get(id)
    return Result.success(data)
@router.post("/sys_menu/syncmenu")
@auth_module(module_name="sys_menu", resource="syncmenu")
async def syncmenu(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    systemcode=jsonData.get('systemcode',None)
    if systemcode is None:
        raise FriendlyException('请传入systemcode')
    dal = MenuBusi(request.state.db)
    result=await dal.SyncMenu(systemcode)
    return Result.success(result)
@router.post("/sys_menu/syncmenu_recive")
@auth_module(module_name="sys_menu", resource="syncmenu_recive")
async def syncmenu_recive(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MenuBusi(request.state.db)
    jsonData = await request.json()
    data = await dal.SynMenuRevice(jsonData)
    return Result.success('同步成功')
@router.post("/sys_menu/init")
@auth_module(module_name="sys_menu", resource="init")
async def mg_menu_init(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MenuBusi(request.state.db)
    jsonData = await request.json()
    await dal.InitMenu(jsonData)
    return Result.success('初始化成功')
@router.post("/sys_menu/init_public")
@auth_module(module_name="sys_menu", resource="init")
async def mg_menu_init_publci(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MenuBusi(request.state.db)
    jsonData = await request.json()
    res=await dal.InitMenuPublic(jsonData)
    return Result.success(res)@router.post("/sys_menu/sync_uimenu")
@auth_module(module_name="sys_menu", resource="sync_uimenu")
async def sync_uimenu(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MenuBusi(request.state.db)
    jsonData = await request.json()
    res=await dal.SyncUIMenu(jsonData)
    return Result.success(res)
