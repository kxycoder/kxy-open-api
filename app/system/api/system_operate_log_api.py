from datetime import datetime
from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.contract.types.send_types import QueryLogFileObject
from app.system.dal.system_operate_log_dal import SystemOperateLogDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_operate_log import SystemOperateLog
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)
from kxy.framework.kxy_logger_filter import QueryCondition,ConditionOperator

@router.get("/operate-log/simple-list")
@auth_schema("system:operate-log:query")
async def system_operate_log_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemOperateLogDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/operate-log/page")
@auth_schema("system:operate-log:query")
async def system_operate_log_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemOperateLogDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/operate-log/create")
@auth_schema("system:operate-log:create")
async def system_operate_log_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOperateLogDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/operate-log/update")
@auth_schema("system:operate-log:update")
async def system_operate_log_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOperateLogDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/operate-log/save")
@auth_schema("system:operate-log:update")
async def system_operate_log_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOperateLogDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/operate-log/delete")
@auth_schema("system:operate-log:delete")
async def system_operate_log_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOperateLogDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/operate-log/delete-list")
@auth_schema("system:operate-log:delete")
async def system_operate_log_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = SystemOperateLogDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/operate-log/get")
@auth_schema("system:operate-log:query")
async def system_operate_log_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOperateLogDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/operate-log/export-excel")
@auth_schema("system:operate-log:export")
async def system_operate_log_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemOperateLogDal(request.state.db)
    await service.ExportExcel(SystemOperateLog,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/sys-log/file-list")
@auth_schema("system:operate-log:export")
async def sys_log_file_list(request: Request,current_user: str = Depends(get_admin_user)):
    datas = logger.get_filtered_files()
    return Result.success(datas)

@router.post("/sys-log/query-log-file")
@auth_schema("system:operate-log:syslog")
async def sys_log_query_log_file(filters:QueryLogFileObject,request: Request,current_user: str = Depends(get_admin_user)):
    conditions = QueryCondition()
    if filters.filters:
        for filter in filters.filters:
            if not filter.oprator:
                conditions = conditions.and_(QueryCondition.eq(filter.key, filter.value))
            else:
                conditions.conditions[filter.key]={ConditionOperator(filter.oprator):filter.value}
    if not filters.start_time:
        filters.start_time = datetime.now().strftime("%Y-%m-%d")
    datas = logger.query(filters.start_time, filters.end_time, conditions)
    return Result.success(datas)