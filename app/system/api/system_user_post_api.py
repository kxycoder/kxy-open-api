from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_user_post_dal import SystemUserPostDal
from app.common.filter import auth_module, get_current_user, get_admin_user,auth_schema
from app.system.models.system_user_post import SystemUserPost
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/user-post/simple-list")
@auth_schema("system:user-post:query")
async def system_user_post_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemUserPostDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/user-post/page")
@auth_schema("system:user-post:query")
async def system_user_post_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemUserPostDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/user-post/create")
@auth_schema("system:user-post:create")
async def system_user_post_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUserPostDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/user-post/update")
@auth_schema("system:user-post:update")
async def system_user_post_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUserPostDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/user-post/save")
@auth_schema("system:user-post:update")
async def system_user_post_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUserPostDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/user-post/delete")
@auth_schema("system:user-post:delete")
async def system_user_post_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUserPostDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/user-post/delete-list")
@auth_schema("system:user-post:delete")
async def system_user_post_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SystemUserPostDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/user-post/get")
@auth_schema("system:user-post:query")
async def system_user_post_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUserPostDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/user-post/export-excel")
@auth_schema("system:user-post:export")
async def system_user_post_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemUserPostDal(request.state.db)
    await service.ExportExcel(SystemUserPost,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")
