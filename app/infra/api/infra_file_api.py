from datetime import datetime
from PIL import Image
import os
import shutil
from uuid import uuid4
from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.infra.dal.infra_file_dal import InfraFileDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.infra.models.infra_file import InfraFile
from app.system.services.excel_service import ExcelService
from app.config import config
from app.infra.services.file_service import FileService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/file/simple-list")
@auth_schema("infra:file:query")
async def infra_file_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = InfraFileDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/file/page")
@auth_schema("infra:file:query")
async def infra_file_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = InfraFileDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/file/create")
@auth_schema("infra:file:create")
async def infra_file_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/file/update")
@auth_schema("infra:file:update")
async def infra_file_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/file/save")
@auth_schema("infra:file:update")
async def infra_file_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/file/delete")
@auth_schema("infra:file:delete")
async def infra_file_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/file/delete-list")
@auth_schema("infra:file:delete")
async def infra_file_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = InfraFileDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/file/get")
@auth_schema("infra:file:query")
async def infra_file_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = InfraFileDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/file/export-excel")
@auth_schema("infra:file:export")
async def infra_file_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = InfraFileDal(request.state.db)
    await service.ExportExcel(InfraFile,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.post("/file/upload")
async def infra_file_upload(request: Request, current_user: str = Depends(get_current_user)):
    form = await request.form()
    file = form.get('file')
    if not file:
        raise FriendlyException('未找到要上传的文件')
    db = request.state.db
    service = FileService(db)
    result = await service.upload(file)
    return Result.success(result)

# /infra/file/25/get/20251010/634d7936-8e35-408e-8e86-949c788838fc.png
@router.get("/file/{id}/get/{filePath:path}")
async def get_file(request: Request, id: int, filePath: str):
    service = FileService(request.state.db)
    file_bytes = await service.get(id, filePath)
    # 根据文件扩展名设置响应类型
    ext = filePath.split('.')[-1].lower()
    content_type = "application/octet-stream"
    if ext in ["jpg", "jpeg"]:
        content_type = "image/jpeg"
    elif ext == "png":
        content_type = "image/png"
    elif ext == "gif":
        content_type = "image/gif"
    return Response(content=file_bytes, media_type=content_type)
