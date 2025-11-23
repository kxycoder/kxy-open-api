from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_sms_log_dal import SystemSmsLogDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_sms_log import SystemSmsLog
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/sms-log/simple-list")
@auth_schema("system:sms-log:query")
async def system_sms_log_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemSmsLogDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/sms-log/page")
@auth_schema("system:sms-log:query")
async def system_sms_log_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemSmsLogDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/sms-log/create")
@auth_schema("system:sms-log:create")
async def system_sms_log_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsLogDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/sms-log/update")
@auth_schema("system:sms-log:update")
async def system_sms_log_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsLogDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/sms-log/save")
@auth_schema("system:sms-log:update")
async def system_sms_log_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsLogDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/sms-log/delete")
@auth_schema("system:sms-log:delete")
async def system_sms_log_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsLogDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/sms-log/delete-list")
@auth_schema("system:sms-log:delete")
async def system_sms_log_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = SystemSmsLogDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/sms-log/get")
@auth_schema("system:sms-log:query")
async def system_sms_log_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsLogDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/sms-log/export-excel")
@auth_schema("system:sms-log:export")
async def system_sms_log_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemSmsLogDal(request.state.db)
    await service.ExportExcel(SystemSmsLog,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")