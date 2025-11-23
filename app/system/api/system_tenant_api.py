from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.contract.types.user_vo import VoUserTenant
from app.common.result import Result
from app.system.dal.system_tenant_dal import SystemTenantDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_tenant import SystemTenant
from app.system.services.tenant_service import TenantService
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/tenant/simple-list")
@auth_schema("system:tenant:query")
async def system_tenant_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemTenantDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/tenant/page")
@auth_schema("system:tenant:query")
async def system_tenant_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemTenantDal(request.state.db)
    search = {**request.query_params}
    
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/tenant/create")
@auth_schema("system:tenant:create")
async def system_tenant_add(data:VoUserTenant,request: Request,current_user: str = Depends(get_admin_user)):
    svc = TenantService(request.state.db)
    data = await svc.CreateTenant(data)
    # data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/tenant/update")
@auth_schema("system:tenant:update")
async def system_tenant_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemTenantDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/tenant/save")
@auth_schema("system:tenant:update")
async def system_tenant_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemTenantDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/tenant/delete")
@auth_schema("system:tenant:delete")
async def system_tenant_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    svc = TenantService(request.state.db)
    await svc.DeleteTenant(id)
    return Result.success("删除成功")
    
@router.delete("/tenant/delete-list")
@auth_schema("system:tenant:delete")
async def system_tenant_deletebatch(request: Request,ids:str,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = SystemTenantDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/tenant/get")
@auth_schema("system:tenant:query")
async def system_tenant_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemTenantDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/tenant/export-excel")
@auth_schema("system:tenant:export")
async def system_tenant_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemTenantDal(request.state.db)
    await service.ExportExcel(SystemTenant,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")
# tenant/get-id-by-name
@router.get("/tenant/get-id-by-name")
async def system_tenant_get_id_by_name(name:str,request: Request):
    dal = SystemTenantDal(request.state.db)
    data =await dal.GetIdByName(name)
    return Result.success(data)