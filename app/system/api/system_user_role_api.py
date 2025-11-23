from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.contract.types.user_vo import VoUserRole
from app.common.result import Result
from app.system.dal.system_user_role_dal import SystemUserRoleDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_user_role import SystemUserRole
from app.system.services.excel_service import ExcelService
router = APIRouter()
from app.system.services.user_service import UserService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/user-role/simple-list")
@auth_schema("system:role:query")
async def system_user_role_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemUserRoleDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/user-role/page")
@auth_schema("system:role:query")
async def system_user_role_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemUserRoleDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/user-role/create")
@auth_schema("system:role:query")
async def system_user_role_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUserRoleDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/user-role/update")
@auth_schema("system:role:query")
async def system_user_role_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUserRoleDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/user-role/save")
async def system_user_role_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUserRoleDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/user-role/delete")
@auth_schema("system:role:query")
async def system_user_role_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUserRoleDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/user-role/delete-list")
@auth_schema("system:role:query")
async def system_user_role_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SystemUserRoleDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/user-role/get")
@auth_schema("system:role:query")
async def system_user_role_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUserRoleDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/user-role/export-excel")
@auth_schema("system:role:export-excel")
async def system_user_role_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemUserRoleDal(request.state.db)
    await service.ExportExcel(SystemUserRole,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/permission/list-user-roles")
@auth_schema("system:role:query")
async def system_user_role_list_user_roles(userId,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUserRoleDal(request.state.db)
    data =await dal.GetUserRoleIds(userId)
    return Result.success(data)

@router.post("/permission/assign-user-role")
@auth_schema("system:permission:assign-user-role")
async def system_user_role_assign_user_role(roles:VoUserRole,request: Request,current_user: str = Depends(get_admin_user)):
    usrSvc = UserService(request.state.db)
    await usrSvc.AssignUserRole(roles)
    return Result.success(True)