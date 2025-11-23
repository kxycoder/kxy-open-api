from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_menu_dal import SystemMenuDal
from app.common.filter import auth_module, get_current_user, get_admin_user,auth_schema
from app.system.models.system_menu import SystemMenu
from app.system.services.excel_service import ExcelService
router = APIRouter()
from app.system.services.menu_service import MenuService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/menu/simple-list")
@auth_schema("system:menu:query")
async def system_menu_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MenuService(request.state.db)
    datas = await dal.GetUserMenu()
    return Result.success(datas)

# system/menu/list
@router.get("/menu/list")
@auth_schema("system:menu:query")
async def system_menu_list1(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemMenuDal(request.state.db)
    search = {**request.query_params}
    data =await dal.GetList(search)
    return Result.success(data)

@router.get("/menu/page")
@auth_schema("system:menu:query")
async def system_menu_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemMenuDal(request.state.db)
    search = {**request.query_params}
    
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/menu/create")
@auth_schema("system:menu:create")
async def system_menu_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemMenuDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/menu/update")
@auth_schema("system:menu:update")
async def system_menu_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemMenuDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/menu/save")
@auth_schema("system:menu:update")
async def system_menu_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemMenuDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/menu/delete")
@auth_schema("system:menu:delete")
async def system_menu_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = MenuService(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/menu/delete-list")
@auth_schema("system:menu:delete")
async def system_menu_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SystemMenuDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/menu/get")
@auth_schema("system:menu:query")
async def system_menu_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemMenuDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/menu/export-excel")
@auth_schema("system:menu:export-excel")
async def system_menu_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemMenuDal(request.state.db)
    await service.ExportExcel(SystemMenu,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/auth/menu_and_actions")
async def menu_and_actions(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MenuService(request.state.db)
    result = await dal.GetUserMenuAndActions()
    return Result.success(result)    

@router.get("/menu/init")
@auth_schema("system:menu:init")
async def system_menu_init(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MenuService(request.state.db)
    await dal.InitMenu()
    return Result.success(True)