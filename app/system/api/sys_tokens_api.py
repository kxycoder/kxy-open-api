# !/usr/bin/python
# -*- coding:utf-8 -*-
import re
import traceback

from fastapi import APIRouter, Depends, Request
router = APIRouter()
from app.common.result import Result
from kxy.framework.friendly_exception import FriendlyException
from app.system.dal.sys_tokens_dal import SysTokensDal
from app.common.filter import auth_module, get_current_user, tryCatch, get_admin_user

@router.get("/sys_tokens/list")
@auth_module(module_name="sys_tokens", resource="list")
async def opt_sso_tokens_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    search = request.query_params.get("search", '')

    dal = SysTokensDal(request.state.db)
    datas,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(datas,total)

@router.post("/sys_tokens/add")
@auth_module(module_name="sys_tokens", resource="add")
async def opt_sso_tokens_add(request: Request,current_user: str = Depends(get_current_user)):
    dal = SysTokensDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)
    return Result.success(data.to_basic_dict())
@router.post("/sys_tokens/update")
@auth_module(module_name="sys_tokens", resource="update")
async def opt_sso_tokens_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = SysTokensDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)
    return Result.success(data.to_basic_dict())
@router.get("/sys_tokens/delete/{id}")
@auth_module(module_name="sys_tokens", resource="delete")
async def opt_sso_tokens_delete(id,request: Request,current_user: str = Depends(get_current_user)):
    dal = SysTokensDal(request.state.db)
    data = await dal.Delete(id)
    return Result.success("删除成功")

@router.get("/sys_tokens/get/{id}")
@auth_module(module_name="sys_tokens", resource="get")
async def opt_sso_tokens_get(id,request: Request,current_user: str = Depends(get_current_user)):
    dal = SysTokensDal(request.state.db)
    data = await dal.Get(id)
    return Result.success(data.to_basic_dict())
