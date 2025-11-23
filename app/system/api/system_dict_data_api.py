from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_dict_data_dal import SystemDictDataDal
from app.common.filter import auth_module, auth_schema, get_current_user, get_admin_user
from app.system.models.system_dict_data import SystemDictData
from app.system.services.dict_service import DictService
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/dict-data/simple-list")
@auth_schema("system:dict-data:query")
async def system_dict_data_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemDictDataDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList()
    return Result.success(datas)

@router.get("/dict-data/page")
@auth_schema("system:dict-data:query")
async def system_dict_data_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemDictDataDal(request.state.db)
    search = {**request.query_params}
    
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/dict-data/create")
@auth_schema("system:dict-data:create")
async def system_dict_data_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = DictService(request.state.db)
    data = await dal.AddDictDataByJson(await request.json())
    return Result.success(data)

@router.put("/dict-data/update")
@auth_schema("system:dict-data:update")
async def system_dict_data_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDictDataDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/dict-data/save")
@auth_schema("system:dict-data:update")
async def system_dict_data_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDictDataDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/dict-data/delete")
@auth_schema("system:dict-data:delete")
async def system_dict_data_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDictDataDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/dict-data/delete-list")
@auth_schema("system:dict-data:delete")
async def system_dict_data_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SystemDictDataDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/dict-data/get")
@auth_schema("system:dict-data:query")
async def system_dict_data_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDictDataDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/dict-data/export-excel")
@auth_schema("system:dict-data:export")
async def system_dict_data_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemDictDataDal(request.state.db)
    await service.ExportExcel(SystemDictData,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

# /dict-data/type
@router.get("/dict-data/type")
@auth_schema("system:dict-data:query")
async def system_dict_data_get_by_type(type,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDictDataDal(request.state.db)
    data =await dal.GetByType(type)
    return Result.success(data)