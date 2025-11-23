import os
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.sys_excel_record_dal import SysExcelRecordDal
from app.common.filter import auth_module, get_current_user, tryCatch, get_admin_user
from kxy.framework.mapper import Mapper
from app.system.models.sys_excel_record import ExcelRecord
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/sys_excel_record/list")
@auth_module(module_name="sys_excel_record", resource="list")
async def excel_record_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    search = {**request.query_params}
    
    dal = SysExcelRecordDal(request.state.db)
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/sys_excel_record/add")
@auth_module(module_name="sys_excel_record", resource="add")
async def excel_record_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysExcelRecordDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.post("/sys_excel_record/update")
@auth_module(module_name="sys_excel_record", resource="update")
async def excel_record_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysExcelRecordDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.get("/sys_excel_record/delete/{id}")
@auth_module(module_name="sys_excel_record", resource="delete")
async def excel_record_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysExcelRecordDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.post("/sys_excel_record/deletebatch")
@auth_module(module_name="sys_excel_record", resource="delete")
async def excel_record_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    keys=request.json.get('keys')
    if keys:
        dal = SysExcelRecordDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/sys_excel_record/get/{id}")
@auth_module(module_name="sys_excel_record", resource="get")
async def excel_record_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysExcelRecordDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/sys_excel_record/export_excel")
@auth_module(module_name="sys_excel_record", resource="export_excel")
async def excel_record_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SysExcelRecordDal(request.state.db)
    await service.ExportExcel(ExcelRecord,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get('/excel')
@auth_module(module_name="sys_excel_record", resource="download_excel")
async def get_file(request: Request,current_user: str = Depends(get_admin_user)):
    id = request.query_params.get('id')
    if not id:
        raise FriendlyException('请传入文件id')
    dal = SysExcelRecordDal(request.state.db)
    exist = await dal.GetExist(id)
    roles = request.state.roles
    if exist.CreateUser != current_user and 'admin' not in roles:
        raise FriendlyException('无权访问该文件')
    root_path = os.path.join(os.getcwd(), 'export_excels')
    file_path = os.path.join(root_path,exist.ExcelFile)
    syslogger = Mapper.getservice('BatchSysLogService')
    await syslogger.AddLogAsync('excel下载', '下载', exist.ExcelFile)
    if os.path.exists(file_path) == False:
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(file_path)