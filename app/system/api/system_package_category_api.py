from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_package_category_dal import SystemPackageCategoryDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_package_category import SystemPackageCategory
from app.system.services.excel_service import ExcelService
router = APIRouter()
from app.system.services.tenant_service import TenantService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/package-category/simple-list")
@auth_schema("system:package-category:query")
async def system_package_category_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemPackageCategoryDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/package-category/page")
@auth_schema("system:package-category:query")
async def system_package_category_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemPackageCategoryDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/package-category/create")
@auth_schema("system:package-category:create")
async def system_package_category_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemPackageCategoryDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/package-category/update")
@auth_schema("system:package-category:update")
async def system_package_category_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemPackageCategoryDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/package-category/save")
@auth_schema("system:package-category:update")
async def system_package_category_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemPackageCategoryDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/package-category/delete")
@auth_schema("system:package-category:delete")
async def system_package_category_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemPackageCategoryDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/package-category/delete-list")
@auth_schema("system:package-category:delete")
async def system_package_category_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = SystemPackageCategoryDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/package-category/get")
@auth_schema("system:package-category:query")
async def system_package_category_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemPackageCategoryDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/package-category/export-excel")
@auth_schema("system:package-category:export")
async def system_package_category_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemPackageCategoryDal(request.state.db)
    await service.ExportExcel(SystemPackageCategory,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/package-category/get-category-items")
@auth_schema("system:package-category:query")
async def system_package_category_get_category_items(categoryName,request: Request,current_user: str = Depends(get_admin_user)):
    service = TenantService(request.state.db)
    data= await service.GetPackageCategory(categoryName)
    return Result.success(data)