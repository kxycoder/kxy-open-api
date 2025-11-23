from typing import List
from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_dict_type_dal import SystemDictTypeDal
from app.common.filter import auth_module, auth_schema, get_current_user, get_admin_user
from app.system.models.system_dict_type import SystemDictType
from app.system.services.dict_service import DictService
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/dict-type/simple-list")
@auth_schema("system:dict-type:query")
async def system_dict_type_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemDictTypeDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/dict-type/page")
@auth_schema("system:dict-type:query")
async def system_dict_type_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemDictTypeDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/dict-type/create")
@auth_schema("system:dict-type:create")
async def system_dict_type_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDictTypeDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/dict-type/update")
@auth_schema("system:dict-type:update")
async def system_dict_type_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDictTypeDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/dict-type/save")
@auth_schema("system:dict-type:update")
async def system_dict_type_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDictTypeDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.post("/dict-type/save-all")
@auth_schema("system:dict-type:update")
async def system_dict_type_save_all(request: Request,current_user: str = Depends(get_admin_user)):
    svc = DictService(request.state.db)
    # dal = SystemDictTypeDal(request.state.db)
    jsonData = await request.json()
    data =await svc.SaveAll(jsonData)
    # if jsonData.get('id'):
    #     data =await dal.UpdateByJsonData(jsonData)
    # else:
    #     data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/dict-type/delete")
@auth_schema("system:dict-type:delete")
async def system_dict_type_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = DictService(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/dict-type/delete-list")
@auth_schema("system:dict-type:delete")
async def system_dict_type_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    # jsonData = await request.json()
    # keys=jsonData.get('keys')
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = DictService(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/dict-type/get")
@auth_schema("system:dict-type:query")
async def system_dict_type_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDictTypeDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/dict-type/export-excel")
@auth_schema("system:dict-type:export")
async def system_dict_type_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemDictTypeDal(request.state.db)
    await service.ExportExcel(SystemDictType,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

