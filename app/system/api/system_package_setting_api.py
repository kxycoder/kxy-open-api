from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_package_setting_dal import SystemPackageSettingDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_package_setting import SystemPackageSetting
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/package-setting/simple-list")
@auth_schema("system:package-setting:query")
async def system_package_setting_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemPackageSettingDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/package-setting/page")
@auth_schema("system:package-setting:query")
async def system_package_setting_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemPackageSettingDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/package-setting/create")
@auth_schema("system:package-setting:create")
async def system_package_setting_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemPackageSettingDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/package-setting/update")
@auth_schema("system:package-setting:update")
async def system_package_setting_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemPackageSettingDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/package-setting/save")
@auth_schema("system:package-setting:update")
async def system_package_setting_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemPackageSettingDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/package-setting/delete")
@auth_schema("system:package-setting:delete")
async def system_package_setting_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemPackageSettingDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/package-setting/delete-list")
@auth_schema("system:package-setting:delete")
async def system_package_setting_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = SystemPackageSettingDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/package-setting/get")
@auth_schema("system:package-setting:query")
async def system_package_setting_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemPackageSettingDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/package-setting/export-excel")
@auth_schema("system:package-setting:export")
async def system_package_setting_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemPackageSettingDal(request.state.db)
    await service.ExportExcel(SystemPackageSetting,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

