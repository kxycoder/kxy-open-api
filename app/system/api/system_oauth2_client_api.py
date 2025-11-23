from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_oauth2_client_dal import SystemOauth2ClientDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_oauth2_client import SystemOauth2Client
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/oauth2-client/simple-list")
@auth_schema("system:oauth2-client:query")
async def system_oauth2_client_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemOauth2ClientDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/oauth2-client/page")
@auth_schema("system:oauth2-client:query")
async def system_oauth2_client_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemOauth2ClientDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/oauth2-client/create")
@auth_schema("system:oauth2-client:create")
async def system_oauth2_client_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2ClientDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/oauth2-client/update")
@auth_schema("system:oauth2-client:update")
async def system_oauth2_client_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2ClientDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/oauth2-client/save")
@auth_schema("system:oauth2-client:update")
async def system_oauth2_client_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2ClientDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/oauth2-client/delete")
@auth_schema("system:oauth2-client:delete")
async def system_oauth2_client_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2ClientDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/oauth2-client/delete-list")
@auth_schema("system:oauth2-client:delete")
async def system_oauth2_client_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = SystemOauth2ClientDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/oauth2-client/get")
@auth_schema("system:oauth2-client:query")
async def system_oauth2_client_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemOauth2ClientDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/oauth2-client/export-excel")
@auth_schema("system:oauth2-client:export")
async def system_oauth2_client_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemOauth2ClientDal(request.state.db)
    await service.ExportExcel(SystemOauth2Client,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/u/oauth2-client/list")
async def usystem_oauth2_client_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = SystemOauth2ClientDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/oauth2-client/add")
async def usystem_oauth2_client_add(request: Request,current_user: str = Depends(get_current_user)):

    dal = SystemOauth2ClientDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)

@router.put("/u/oauth2-client/update")
async def usystem_oauth2_client_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemOauth2ClientDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)

@router.post("/u/oauth2-client/save")
async def usystem_oauth2_client_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemOauth2ClientDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)

@router.delete("/u/oauth2-client/delete")
async def usystem_oauth2_client_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemOauth2ClientDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/oauth2-client/get")
async def usystem_oauth2_client_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemOauth2ClientDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)