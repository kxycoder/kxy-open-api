from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.infra.dal.infra_file_content_dal import InfraFileContentDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.infra.models.infra_file_content import InfraFileContent
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/file-content/simple-list")
@auth_schema("infra:file-content:query")
async def infra_file_content_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = InfraFileContentDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/file-content/page")
@auth_schema("infra:file-content:query")
async def infra_file_content_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = InfraFileContentDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/file-content/create")
@auth_schema("infra:file-content:create")
async def infra_file_content_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileContentDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/file-content/update")
@auth_schema("infra:file-content:update")
async def infra_file_content_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileContentDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/file-content/save")
@auth_schema("infra:file-content:update")
async def infra_file_content_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileContentDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/file-content/delete")
@auth_schema("infra:file-content:delete")
async def infra_file_content_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileContentDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/file-content/delete-list")
@auth_schema("infra:file-content:delete")
async def infra_file_content_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = InfraFileContentDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/file-content/get")
@auth_schema("infra:file-content:query")
async def infra_file_content_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileContentDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/file-content/export-excel")
@auth_schema("infra:file-content:export")
async def infra_file_content_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = InfraFileContentDal(request.state.db)
    await service.ExportExcel(InfraFileContent,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")