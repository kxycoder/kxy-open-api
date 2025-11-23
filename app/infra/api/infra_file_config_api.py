from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.infra.dal.infra_file_config_dal import InfraFileConfigDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.infra.models.infra_file_config import InfraFileConfig
from app.infra.services.file_service import FileService
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/file-config/simple-list")
@auth_schema("infra:file-config:query")
async def infra_file_config_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = InfraFileConfigDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/file-config/page")
@auth_schema("infra:file-config:query")
async def infra_file_config_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = InfraFileConfigDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/file-config/create")
@auth_schema("infra:file-config:create")
async def infra_file_config_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileConfigDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/file-config/update")
@auth_schema("infra:file-config:update")
async def infra_file_config_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileConfigDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/file-config/save")
@auth_schema("infra:file-config:update")
async def infra_file_config_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileConfigDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/file-config/delete")
@auth_schema("infra:file-config:delete")
async def infra_file_config_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileConfigDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/file-config/delete-list")
@auth_schema("infra:file-config:delete")
async def infra_file_config_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = InfraFileConfigDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/file-config/get")
@auth_schema("infra:file-config:query")
async def infra_file_config_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileConfigDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/file-config/export-excel")
@auth_schema("infra:file-config:export")
async def infra_file_config_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = InfraFileConfigDal(request.state.db)
    await service.ExportExcel(InfraFileConfig,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

# /api/infra/file-config/update-master?id=25
@router.put("/file-config/update-master")
@auth_schema("infra:file-config:update")
async def infra_file_config_update_master(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    await FileService(request.state.db).UpdateDeafultUploadConfig(id)
    return Result.success("更新成功")