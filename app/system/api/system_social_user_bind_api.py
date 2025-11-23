from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_social_user_bind_dal import SystemSocialUserBindDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_social_user_bind import SystemSocialUserBind
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/social-user-bind/simple-list")
@auth_schema("system:social-user-bind:query")
async def system_social_user_bind_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemSocialUserBindDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/social-user-bind/page")
@auth_schema("system:social-user-bind:query")
async def system_social_user_bind_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemSocialUserBindDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/social-user-bind/create")
@auth_schema("system:social-user-bind:create")
async def system_social_user_bind_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSocialUserBindDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/social-user-bind/update")
@auth_schema("system:social-user-bind:update")
async def system_social_user_bind_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSocialUserBindDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/social-user-bind/save")
@auth_schema("system:social-user-bind:update")
async def system_social_user_bind_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSocialUserBindDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/social-user-bind/delete")
@auth_schema("system:social-user-bind:delete")
async def system_social_user_bind_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSocialUserBindDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/social-user-bind/delete-list")
@auth_schema("system:social-user-bind:delete")
async def system_social_user_bind_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = SystemSocialUserBindDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/social-user-bind/get")
@auth_schema("system:social-user-bind:query")
async def system_social_user_bind_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSocialUserBindDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/social-user-bind/export-excel")
@auth_schema("system:social-user-bind:export")
async def system_social_user_bind_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemSocialUserBindDal(request.state.db)
    await service.ExportExcel(SystemSocialUserBind,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")