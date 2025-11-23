from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_role_menu_dal import SystemRoleMenuDal
from app.common.filter import auth_module, auth_schema, get_current_user, get_admin_user
from app.system.models.system_role_menu import SystemRoleMenu
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/permission/simple-list")
@auth_module(module_name="system_role_menu", resource="list")
async def system_role_menu_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemRoleMenuDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/permission/page")
@auth_module(module_name="system_role_menu", resource="list")
async def system_role_menu_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemRoleMenuDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/permission/create")
@auth_module(module_name="system_role_menu", resource="add")
async def system_role_menu_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemRoleMenuDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/permission/update")
@auth_module(module_name="system_role_menu", resource="update")
async def system_role_menu_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemRoleMenuDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/permission/save")
async def system_role_menu_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemRoleMenuDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/permission/delete")
@auth_module(module_name="system_role_menu", resource="delete")
async def system_role_menu_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemRoleMenuDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/permission/delete-list")
@auth_module(module_name="system_role_menu", resource="delete")
async def system_role_menu_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SystemRoleMenuDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/permission/get")
@auth_module(module_name="system_role_menu", resource="get")
async def system_role_menu_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemRoleMenuDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/permission/export-excel")
@auth_module(module_name="system_role_menu", resource="export_excel")
async def system_role_menu_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemRoleMenuDal(request.state.db)
    await service.ExportExcel(SystemRoleMenu,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

# /permission/list-role-menus
@router.get("/permission/list-role-menus")
@auth_module(module_name="system_role_menu", resource="list_role_menus")
async def system_role_menu_list_role_menus(roleId:str,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemRoleMenuDal(request.state.db)
    data =await dal.ListRoleMenus(roleId)
    return Result.success(data)

