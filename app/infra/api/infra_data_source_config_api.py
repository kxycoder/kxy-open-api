from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.infra.dal.infra_data_source_config_dal import InfraDataSourceConfigDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.infra.models.infra_data_source_config import InfraDataSourceConfig
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/data-source-config/list")
@auth_schema("infra:data-source-config:query")
async def infra_data_source_config_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = InfraDataSourceConfigDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/data-source-config/page")
@auth_schema("infra:data-source-config:query")
async def infra_data_source_config_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = InfraDataSourceConfigDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/data-source-config/create")
@auth_schema("infra:data-source-config:create")
async def infra_data_source_config_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraDataSourceConfigDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/data-source-config/update")
@auth_schema("infra:data-source-config:update")
async def infra_data_source_config_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraDataSourceConfigDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/data-source-config/save")
@auth_schema("infra:data-source-config:update")
async def infra_data_source_config_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraDataSourceConfigDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/data-source-config/delete")
@auth_schema("infra:data-source-config:delete")
async def infra_data_source_config_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraDataSourceConfigDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/data-source-config/delete-list")
@auth_schema("infra:data-source-config:delete")
async def infra_data_source_config_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = InfraDataSourceConfigDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/data-source-config/get")
@auth_schema("infra:data-source-config:query")
async def infra_data_source_config_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraDataSourceConfigDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/data-source-config/export-excel")
@auth_schema("infra:data-source-config:export")
async def infra_data_source_config_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = InfraDataSourceConfigDal(request.state.db)
    await service.ExportExcel(InfraDataSourceConfig,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")
