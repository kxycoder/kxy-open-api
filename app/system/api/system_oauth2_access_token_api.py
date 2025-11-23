from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_oauth2_access_token_dal import SystemOauth2AccessTokenDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_oauth2_access_token import SystemOauth2AccessToken
from app.system.services.excel_service import ExcelService
router = APIRouter()
from app.system.services.user_service import UserService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/oauth2-token/simple-list")
@auth_schema("system:oauth2-token:query")
async def system_oauth2_access_token_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemOauth2AccessTokenDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/oauth2-token/page")
@auth_schema("system:oauth2-token:query")
async def system_oauth2_access_token_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemOauth2AccessTokenDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/oauth2-token/create")
@auth_schema("system:oauth2-token:create")
async def system_oauth2_access_token_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2AccessTokenDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/oauth2-token/update")
@auth_schema("system:oauth2-token:update")
async def system_oauth2_access_token_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2AccessTokenDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/oauth2-token/save")
@auth_schema("system:oauth2-token:update")
async def system_oauth2_access_token_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2AccessTokenDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/oauth2-token/delete")
@auth_schema("system:oauth2-token:delete")
async def system_oauth2_access_token_delete(accessToken:str,request: Request,current_user: str = Depends(get_admin_user)):
    svc = UserService(request.state.db)
    await svc.DeleleteAccessToken(accessToken)
    logger.info(f"删除{accessToken}成功")
    return Result.success(True)
@router.get("/oauth2-token/get")
@auth_schema("system:oauth2-token:query")
async def system_oauth2_access_token_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2AccessTokenDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/oauth2-token/export-excel")
@auth_schema("system:oauth2-token:export")
async def system_oauth2_access_token_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemOauth2AccessTokenDal(request.state.db)
    await service.ExportExcel(SystemOauth2AccessToken,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")
