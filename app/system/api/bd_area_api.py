# !/usr/bin/python
# -*- coding:utf-8 -*-
import re
import traceback



from fastapi import APIRouter, Depends, Request
router = APIRouter()

from app.common.result import Result
from kxy.framework.friendly_exception import FriendlyException
from app.system.dal.bd_area_dal import BdAreaDal
# from app.common import Util
from app.common.filter import auth_module, get_admin_user, get_admin_user

@router.get("/sys_area/list")
async def bd_area_list(request: Request,current_user: str = Depends(get_admin_user)):
    try:
        PageIndex = int(request.query_params.get("current", 1))
        PageLimit = int(request.query_params.get("pageSize", 10))
        
        dal = BdAreaDal(request.state.db)
        total,data = await dal.List(request.query_params,PageIndex, PageLimit)
        return Result.antd_success(total,data)
    except FriendlyException as fex:
        return Result.friendlyerror(str(fex))
    except Exception as ex:
        return Result.error(traceback.format_exc(limit=1))

@router.get("/sys_area/getchildrens")
async def bd_area_getchildrens(request: Request,current_user: str = Depends(get_admin_user)):
    try:
        pId=request.query_params.get('pId',0)
        if pId=='':
            pId=0
        dal = BdAreaDal(request.state.db)
        data = await dal.GetChildrens(pId)
        return Result.ant_list_success(data)
    except FriendlyException as fex:
        return Result.friendlyerror(str(fex))
    except Exception as ex:
        return Result.error(traceback.format_exc(limit=1))

@router.post("/sys_area/add")
@auth_module(module_name="sys_area", resource="add")
async def bd_area_add(request: Request,current_user: str = Depends(get_admin_user)):
    try:
        dal = BdAreaDal(request.state.db)
        jsonData = await request.json()
        data = await dal.AddByJsonData(jsonData)
        return Result.success(data.to_basic_dict())
    except FriendlyException as fex:
        return Result.friendlyerror(str(fex))
    except Exception as ex:
        return Result.error(traceback.format_exc(limit=1))

@router.post("/sys_area/update")
@auth_module(module_name="sys_area", resource="update")
async def bd_area_update(request: Request,current_user: str = Depends(get_admin_user)):
    try:
        dal = BdAreaDal(request.state.db)
        jsonData = await request.json()
        data = await dal.UpdateByJsonData(jsonData)
        return Result.success(data.to_basic_dict())
    except FriendlyException as fex:
        return Result.friendlyerror(str(fex))
    except Exception as ex:
        return Result.error(traceback.format_exc(limit=1))

@router.get("/sys_area/delete/{id}")
@auth_module(module_name="sys_area", resource="delete")
async def bd_area_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    try:
        dal = BdAreaDal(request.state.db)
        data = await dal.Delete(id)
        return Result.success("删除成功")
    except FriendlyException as fex:
        return Result.friendlyerror(str(fex))
    except Exception as ex:
        return Result.error(traceback.format_exc(limit=1))
    
@router.post("/sys_area/deletebatch")
@auth_module(module_name="sys_area", resource="delete")
async def bd_area_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    try:
        jsonData = await request.json()
        keys=jsonData.get('key')
        if keys:
            dal = BdAreaDal(request.state.db)
            await dal.deletebatch(keys)
            return Result.success("删除成功")
        else:
            raise FriendlyException('请传入要删除的行')
    except FriendlyException as fex:
        return Result.friendlyerror(str(fex))
    except Exception as ex:
        return Result.error(traceback.format_exc(limit=1))

@router.get("/sys_area/get/{id}")
@auth_module(module_name="sys_area", resource="get")
async def bd_area_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    try:
        dal = BdAreaDal(request.state.db)
        data = await dal.Get(id)
        return Result.success(data.to_basic_dict())
    except FriendlyException as fex:
        return Result.friendlyerror(str(fex))
    except Exception as ex:
        return Result.error(traceback.format_exc(limit=1))
