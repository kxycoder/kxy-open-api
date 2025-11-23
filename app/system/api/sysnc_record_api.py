# !/usr/bin/python
# -*- coding:utf-8 -*-
import traceback
from fastapi import APIRouter, Depends, Request

router = APIRouter()
from app.common.result import Result
from kxy.framework.friendly_exception import FriendlyException
from app.system.dal.sysnc_record_dal import SysncRecordDal
from app.common.filter import auth_module, get_admin_user

@router.get("/sysnc_record/list")

@auth_module(module_name="sysnc_record", resource="list")
async def sysnc_record_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = SysncRecordDal(request.state.db)
    datas,total =await dal.List(request.query_params,PageIndex, PageLimit)
    return Result.pagesuccess(datas,total)

@router.post("/sysnc_record/add")
@auth_module(module_name="sysnc_record", resource="add")
async def sysnc_record_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysncRecordDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)
    return Result.success(data.to_basic_dict())
@router.post("/sysnc_record/update")
@auth_module(module_name="sysnc_record", resource="update")
async def sysnc_record_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysncRecordDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)
    return Result.success(data.to_basic_dict())
@router.get("/sysnc_record/delete/{id}")
@auth_module(module_name="sysnc_record", resource="delete")
async def sysnc_record_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysncRecordDal(request.state.db)
    data =await dal.Delete(id)
    return Result.success("删除成功")
@router.get("/sysnc_record/get/{id}")
@auth_module(module_name="sysnc_record", resource="get")
async def sysnc_record_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysncRecordDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data.to_basic_dict())
