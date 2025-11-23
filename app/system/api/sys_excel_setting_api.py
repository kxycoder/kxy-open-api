from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.sys_excel_setting_dal import SysExcelSettingDal
from app.common.filter import auth_module, get_current_user, tryCatch, get_admin_user
from app.system.models.sys_excel_setting import ExcelSetting
from app.system.services.excel_service import ExcelService
from app.system.services.mysql_service import MysqlService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/sys_excel_setting/list")
@auth_module(module_name="sys_excel_setting", resource="list")
async def excel_setting_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = SysExcelSettingDal(request.state.db)
    data,total =await dal.Search(request.query_params,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/sys_excel_setting/add")
@auth_module(module_name="sys_excel_setting", resource="add")
async def excel_setting_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ExcelService(request.state.db)
    data = await dal.AddSetting(await request.json())
    return Result.success(data)

@router.post("/sys_excel_setting/update")
@auth_module(module_name="sys_excel_setting", resource="update")
async def excel_setting_update(request: Request,current_user: str = Depends(get_admin_user)):
    svc = ExcelService(request.state.db)
    data = await svc.UpdateSetting(await request.json())
    return Result.success(data)

@router.get("/sys_excel_setting/delete/{id}")
@auth_module(module_name="sys_excel_setting", resource="delete")
async def excel_setting_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysExcelSettingDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.post("/sys_excel_setting/deletebatch")
@auth_module(module_name="sys_excel_setting", resource="delete")
async def excel_setting_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    keys=request.json.get('keys')
    if keys:
        dal = SysExcelSettingDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/sys_excel_setting/get/{id}")
@auth_module(module_name="sys_excel_setting", resource="get")
async def excel_setting_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysExcelSettingDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/sys_excel_setting/export_excel")
@auth_module(module_name="sys_excel_setting", resource="export_excel")
async def excel_setting_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SysExcelSettingDal(request.state.db)
    await service.ExportExcel(ExcelSetting,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/sys_excel_setting/table_list")
@auth_module(module_name="sys_excel_setting", resource="add")
async def excel_setting_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = MysqlService(request.state.db)
    data = await service.get_tables()
    return Result.success(data)