# !/usr/bin/python
# -*- coding:utf-8 -*-
import re
import traceback

from fastapi import APIRouter, Depends, Request
router = APIRouter()

from app.config import config
from app.common.result import Result
from kxy.framework.friendly_exception import FriendlyException
from app.system.dal.sys_system_dal import SysSystemDal

from app.common.filter import auth_module, get_admin_user
from app.system.services.menu_busi import MenuBusi
from app.common.filter import getRoles
@router.get("/sys_system/list")
@auth_module(module_name="sys_system", resource="list")
async def mg_system_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    search = request.query_params.get("search", '')

    dal = SysSystemDal(request.state.db)
    roles = getRoles()
    datas,total = await dal.List(search,roles,PageIndex, PageLimit)
    return Result.pagesuccess(datas,total)
@router.get("/sys_system/getmysystem")
@auth_module(module_name="sys_system", resource="list")
async def mg_system_getmysystem(request: Request,current_user: str = Depends(get_admin_user)):
    userid=current_user
    if config.ignor_auth:
        dal = SysSystemDal(request.state.db)
        data  = await dal.GetAllSystem()
    else:
        busi = MenuBusi(request.state.db)
        data=await busi.GetUserEnableSysmteCode(userid) 
    return Result.success(data)
@router.post("/sys_system/add")
@auth_module(module_name="sys_system", resource="add")
async def mg_system_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MenuBusi(request.state.db)
    jsonData = await request.json()
    data = await dal.AddSystemCode(jsonData)
    return Result.success(data)
@router.post("/sys_system/update")
@auth_module(module_name="sys_system", resource="update")
async def mg_system_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysSystemDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)
    return Result.success(data)
@router.get("/sys_system/delete/{id}")
@auth_module(module_name="sys_system", resource="delete")
async def mg_system_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysSystemDal(request.state.db)
    data = await dal.Delete(id)
    return Result.success("删除成功")
router.get("/sys_system/get/{id}")
@auth_module(module_name="sys_system", resource="get")
async def mg_system_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysSystemDal(request.state.db)
    data = await dal.Get(id)
    return Result.success(data)
@router.post("/sys_system/clearcache")
@auth_module(module_name="sys_system", resource="clearcache")
async def mg_system_clearcache(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    systemcode=jsonData.get('systemcode',None)
    if systemcode=='': 
        raise FriendlyException('请传入systemcode')
    dal = MenuBusi(request.state.db)
    await dal.ClearSystemCodeCache(systemcode)
    return Result.success('成功清理')
