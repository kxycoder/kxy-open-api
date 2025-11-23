from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.infra.dal.infra_publish_version_dal import InfraPublishVersionDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.infra.models.infra_publish_version import InfraPublishVersion
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/publish-version/simple-list")
@auth_schema("infra:publish-version:query")
async def infra_publish_version_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = InfraPublishVersionDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/publish-version/page")
@auth_schema("infra:publish-version:query")
async def infra_publish_version_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = InfraPublishVersionDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/publish-version/create")
@auth_schema("infra:publish-version:create")
async def infra_publish_version_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraPublishVersionDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/publish-version/update")
@auth_schema("infra:publish-version:update")
async def infra_publish_version_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraPublishVersionDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/publish-version/save")
@auth_schema("infra:publish-version:update")
async def infra_publish_version_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraPublishVersionDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/publish-version/delete")
@auth_schema("infra:publish-version:delete")
async def infra_publish_version_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraPublishVersionDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")

@router.delete("/publish-version/delete-list")
@auth_schema("infra:publish-version:delete")
async def infra_publish_version_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = InfraPublishVersionDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/publish-version/get")
@auth_schema("infra:publish-version:query")
async def infra_publish_version_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraPublishVersionDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/publish-version/export-excel")
@auth_schema("infra:publish-version:export")
async def infra_publish_version_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = InfraPublishVersionDal(request.state.db)
    await service.ExportExcel(InfraPublishVersion,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/publish_version/get_version")
async def publish_version_get_version(appName:str,request: Request):
    versionType = request.query_params.get("versionType","date")
    if not appName or not versionType:
        raise FriendlyException('请传入appName和appType')
    dal = InfraPublishVersionDal(request.state.db)
    data = await dal.GetVersionByAppName(appName,versionType)
    return {"Version":data.version,"PreVersion":data.preVersion}