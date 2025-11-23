from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_role_dal import SystemRoleDal
from app.common.filter import auth_module, get_current_user, get_admin_user,auth_schema
from app.system.dal.system_role_menu_dal import SystemRoleMenuDal
from app.system.models.system_role import SystemRole
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/role/simple-list")
@auth_schema("system:role:query")
async def system_role_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemRoleDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/role/page")
@auth_schema("system:role:query")
async def system_role_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemRoleDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/role/create")
@auth_schema("system:role:create")
async def system_role_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemRoleDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/role/update")
@auth_schema("system:role:update")
async def system_role_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemRoleDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/role/save")
@auth_schema("system:role:update")
async def system_role_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemRoleDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/role/delete")
@auth_schema("system:role:delete")
async def system_role_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemRoleDal(request.state.db)
    exist = await dal.Get(id)
    if exist and exist.type == 1:
        raise FriendlyException("内置角色不能删除")
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/role/delete-list")
@auth_schema("system:role:delete")
async def system_role_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SystemRoleDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/role/get")
@auth_schema("system:role:query")
async def system_role_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemRoleDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/role/export-excel")
@auth_schema("system:role:export")
async def system_role_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemRoleDal(request.state.db)
    await service.ExportExcel(SystemRole,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.post("/permission/assign-role-data-scope")
@auth_schema("system:permission:assign-role-data-scope")
async def system_role_assign_role_data_scope(request: Request,current_user: str = Depends(get_admin_user)):
    # {"roleId":159,"dataScope":2,"dataScopeDeptIds":[100,101,112,103,104,105,106,107,102,113]}
    data = await request.json()
    dal = SystemRoleDal(request.state.db)
    data =await dal.assign_role_data_scope(data['roleId'],data['dataScope'],data['dataScopeDeptIds'])
    return Result.success(data)

@router.post("/permission/assign-role-menu")
@auth_schema("system:permission:assign-role-data-scope")
async def system_role_menu_assign_role_menu(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    roleId = jsonData.get('roleId')
    menuIds = jsonData.get('menuIds')
    dal = SystemRoleMenuDal(request.state.db)
    # todo 增加缓存
    # await dal.DeleteBatchByRoleId(roleId)
    await dal.AssignRoleMenus(roleId,menuIds)
    return Result.success(True)