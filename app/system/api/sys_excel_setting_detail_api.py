from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.sys_excel_setting_detail_dal import SysExcelSettingDetailDal
from app.common.filter import auth_module, get_current_user, tryCatch, get_admin_user
from app.system.models.sys_excel_setting_detail import ExcelSettingDetail
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/sys_excel_setting_detail/list")
@auth_module(module_name="sys_excel_setting_detail", resource="list")
async def excel_setting_detail_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = SysExcelSettingDetailDal(request.state.db)
    data,total =await dal.Search(request.query_params,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/sys_excel_setting_detail/add")
@auth_module(module_name="sys_excel_setting_detail", resource="add")
async def excel_setting_detail_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysExcelSettingDetailDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.post("/sys_excel_setting_detail/update")
@auth_module(module_name="sys_excel_setting_detail", resource="update")
async def excel_setting_detail_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysExcelSettingDetailDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.get("/sys_excel_setting_detail/delete/{id}")
@auth_module(module_name="sys_excel_setting_detail", resource="delete")
async def excel_setting_detail_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysExcelSettingDetailDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.post("/sys_excel_setting_detail/deletebatch")
@auth_module(module_name="sys_excel_setting_detail", resource="delete")
async def excel_setting_detail_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    keys=request.json.get('keys')
    if keys:
        dal = SysExcelSettingDetailDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/sys_excel_setting_detail/get/{id}")
@auth_module(module_name="sys_excel_setting_detail", resource="get")
async def excel_setting_detail_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysExcelSettingDetailDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/sys_excel_setting_detail/export_excel")
@auth_module(module_name="sys_excel_setting_detail", resource="export_excel")
async def excel_setting_detail_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SysExcelSettingDetailDal(request.state.db)
    await service.ExportExcel(ExcelSettingDetail,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/u/sys_excel_setting_detail/list")
async def uexcel_setting_detail_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = SysExcelSettingDetailDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit)
    return Result.pagesuccess(datas,total)

# @router.post("/u/sys_excel_setting_detail/add")
# async def uexcel_setting_detail_add(request: Request,current_user: str = Depends(get_current_user)):

#     dal = ExcelSettingDetailDal(request.state.db)
#     data =await dal.AddByJsonDataUser(await request.json())
#     return Result.success(data)

# @router.post("/u/sys_excel_setting_detail/update")
# async def uexcel_setting_detail_update(request: Request,current_user: str = Depends(get_current_user)):
#     dal = ExcelSettingDetailDal(request.state.db)
#     data =await dal.UpdateByJsonDataUser(await request.json())
#     return Result.success(data)

# @router.get("/u/sys_excel_setting_detail/delete/{id}")
# async def uexcel_setting_detail_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
#     dal = ExcelSettingDetailDal(request.state.db)
#     data =await dal.DeleteByUser(id)
#     return Result.success("删除成功")
        
@router.get("/u/sys_excel_setting_detail/get/{id}")
async def uexcel_setting_detail_get(id:str,request: Request,current_user: str = Depends(get_current_user)):
    dal = SysExcelSettingDetailDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)