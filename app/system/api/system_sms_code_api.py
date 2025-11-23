from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_sms_code_dal import SystemSmsCodeDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_sms_code import SystemSmsCode
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/sms-code/simple-list")
@auth_schema("system:sms-code:query")
async def system_sms_code_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemSmsCodeDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/sms-code/page")
@auth_schema("system:sms-code:query")
async def system_sms_code_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemSmsCodeDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/sms-code/create")
@auth_schema("system:sms-code:create")
async def system_sms_code_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsCodeDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/sms-code/update")
@auth_schema("system:sms-code:update")
async def system_sms_code_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsCodeDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/sms-code/save")
@auth_schema("system:sms-code:update")
async def system_sms_code_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsCodeDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/sms-code/delete")
@auth_schema("system:sms-code:delete")
async def system_sms_code_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsCodeDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/sms-code/delete-list")
@auth_schema("system:sms-code:delete")
async def system_sms_code_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = SystemSmsCodeDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/sms-code/get")
@auth_schema("system:sms-code:query")
async def system_sms_code_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsCodeDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/sms-code/export-excel")
@auth_schema("system:sms-code:export")
async def system_sms_code_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemSmsCodeDal(request.state.db)
    await service.ExportExcel(SystemSmsCode,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")