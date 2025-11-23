from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_oauth2_refresh_token_dal import SystemOauth2RefreshTokenDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_oauth2_refresh_token import SystemOauth2RefreshToken
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/system-oauth2-refresh-token/simple-list")
@auth_schema("system:system-oauth2-refresh-token:query")
async def system_oauth2_refresh_token_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemOauth2RefreshTokenDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/system-oauth2-refresh-token/page")
@auth_schema("system:system-oauth2-refresh-token:query")
async def system_oauth2_refresh_token_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemOauth2RefreshTokenDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/system-oauth2-refresh-token/create")
@auth_schema("system:system-oauth2-refresh-token:create")
async def system_oauth2_refresh_token_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2RefreshTokenDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/system-oauth2-refresh-token/update")
@auth_schema("system:system-oauth2-refresh-token:update")
async def system_oauth2_refresh_token_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2RefreshTokenDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/system-oauth2-refresh-token/save")
@auth_schema("system:system-oauth2-refresh-token:update")
async def system_oauth2_refresh_token_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2RefreshTokenDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/system-oauth2-refresh-token/delete")
@auth_schema("system:system-oauth2-refresh-token:delete")
async def system_oauth2_refresh_token_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2RefreshTokenDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/system-oauth2-refresh-token/delete-list")
@auth_schema("system:system-oauth2-refresh-token:delete")
async def system_oauth2_refresh_token_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = SystemOauth2RefreshTokenDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/system-oauth2-refresh-token/get")
@auth_schema("system:system-oauth2-refresh-token:query")
async def system_oauth2_refresh_token_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2RefreshTokenDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/system-oauth2-refresh-token/export-excel")
@auth_schema("system:system-oauth2-refresh-token:export")
async def system_oauth2_refresh_token_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemOauth2RefreshTokenDal(request.state.db)
    await service.ExportExcel(SystemOauth2RefreshToken,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")