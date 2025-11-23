from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_notice_dal import SystemNoticeDal
from app.common.filter import auth_module, auth_schema, get_current_user, get_admin_user
from app.system.models.system_notice import SystemNotice
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/notice/simple-list")
@auth_schema("system:notice:query")
async def system_notice_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemNoticeDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/notice/page")
@auth_schema("system:notice:query")
async def system_notice_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemNoticeDal(request.state.db)
    search = {**request.query_params}
    
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/notice/create")
@auth_schema("system:notice:create")
async def system_notice_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNoticeDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/notice/update")
@auth_schema("system:notice:update")
async def system_notice_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNoticeDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/notice/save")
@auth_schema("system:notice:update")
async def system_notice_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNoticeDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/notice/delete")
@auth_schema("system:notice:delete")
async def system_notice_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNoticeDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/notice/delete-list")
@auth_schema("system:notice:delete")
async def system_notice_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SystemNoticeDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/notice/get")
@auth_schema("system:notice:query")
async def system_notice_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNoticeDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/notice/export-excel")
@auth_schema("system:notice:export")
async def system_notice_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemNoticeDal(request.state.db)
    await service.ExportExcel(SystemNotice,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")
