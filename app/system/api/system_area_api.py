from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_area_dal import SystemAreaDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_area import SystemArea
from app.system.services.excel_service import ExcelService
router = APIRouter()
from app.tools import utils
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/area/simple-list")
@auth_schema("system:area:query")
async def system_area_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemAreaDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/area/tree")
@auth_schema("system:area:query")
async def system_area_tree(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemAreaDal(request.state.db)
    datas = await dal.GetSimpleListAll()
    if datas:
        datas = utils.tree(datas)
    return Result.success(datas)

@router.get("/area/init")
@auth_schema("system:area:create")
async def system_area_tree(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemAreaDal(request.state.db)
    await dal.init()
    return Result.success(True)


@router.get("/area/page")
@auth_schema("system:area:query")
async def system_area_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemAreaDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/area/create")
@auth_schema("system:area:create")
async def system_area_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemAreaDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/area/update")
@auth_schema("system:area:update")
async def system_area_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemAreaDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/area/save")
@auth_schema("system:area:update")
async def system_area_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemAreaDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/area/delete")
@auth_schema("system:area:delete")
async def system_area_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemAreaDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/area/delete-list")
@auth_schema("system:area:delete")
async def system_area_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = SystemAreaDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/area/get")
@auth_schema("system:area:query")
async def system_area_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemAreaDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/area/export-excel")
@auth_schema("system:area:export")
async def system_area_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemAreaDal(request.state.db)
    await service.ExportExcel(SystemArea,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/u/area/list")
async def usystem_area_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = SystemAreaDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/area/add")
async def usystem_area_add(request: Request,current_user: str = Depends(get_current_user)):

    dal = SystemAreaDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)

@router.put("/u/area/update")
async def usystem_area_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemAreaDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)

@router.post("/u/area/save")
async def usystem_area_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemAreaDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)

@router.delete("/u/area/delete")
async def usystem_area_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemAreaDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/area/get")
async def usystem_area_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemAreaDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)