from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.contract.types.send_types import QueryLogFileObject
from app.system.dal.sys_log_dal import SysLogDal
from app.common.filter import auth_module, get_current_user, tryCatch, get_admin_user
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)
from kxy.framework.kxy_logger_filter import QueryCondition,ConditionOperator

@router.get("/sys_log/list")
@auth_module(module_name="sys_log", resource="list")
async def sys_log_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = SysLogDal(request.state.db)
    data,total =await dal.Search(request.query_params,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)


@router.post("/sys_log/add")
@auth_module(module_name="sys_log", resource="add")
async def sys_log_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysLogDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.post("/sys_log/update")
@auth_module(module_name="sys_log", resource="update")
async def sys_log_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysLogDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.get("/sys_log/delete/{id}")
@auth_module(module_name="sys_log", resource="delete")
async def sys_log_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysLogDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.post("/sys_log/deletebatch")
@auth_module(module_name="sys_log", resource="delete")
async def sys_log_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    keys=request.json.get('keys')
    if keys:
        dal = SysLogDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/sys_log/get/{id}")
@auth_module(module_name="sys_log", resource="get")
async def sys_log_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysLogDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)