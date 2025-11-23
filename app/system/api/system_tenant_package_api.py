import json
from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_tenant_package_dal import SystemTenantPackageDal
from app.common.filter import auth_module, auth_schema, get_current_user, get_admin_user
from app.system.models.system_tenant_package import SystemTenantPackage
from app.system.services.excel_service import ExcelService
router = APIRouter()
from app.system.services.tenant_service import TenantService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/tenant-package/simple-list")
@auth_schema("system:tenant-package:query")
async def system_tenant_package_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemTenantPackageDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/tenant-package/page")
@auth_schema("system:tenant-package:query")
async def system_tenant_package_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemTenantPackageDal(request.state.db)
    search = {**request.query_params}
    
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/tenant-package/create")
@auth_schema("system:tenant-package:create")
async def system_tenant_package_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemTenantPackageDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/tenant-package/update")
@auth_schema("system:tenant-package:update")
async def system_tenant_package_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TenantService(request.state.db)
    data = await dal.UpdatePackage(await request.json())
    return Result.success(data)

@router.post("/tenant-package/save")
@auth_schema("system:tenant-package:update")
async def system_tenant_package_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemTenantPackageDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/tenant-package/delete")
@auth_schema("system:tenant-package:delete")
async def system_tenant_package_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemTenantPackageDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/tenant-package/delete-list")
@auth_schema("system:tenant-package:delete")
async def system_tenant_package_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SystemTenantPackageDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/tenant-package/get")
@auth_schema("system:tenant-package:query")
async def system_tenant_package_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemTenantPackageDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/tenant-package/export-excel")
@auth_schema("system:tenant-package:export")
async def system_tenant_package_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemTenantPackageDal(request.state.db)
    await service.ExportExcel(SystemTenantPackage,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")
