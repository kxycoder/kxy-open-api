from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_notify_message_dal import SystemNotifyMessageDal
from app.common.filter import auth_module, auth_schema, get_current_user, get_admin_user
from app.system.models.system_notify_message import SystemNotifyMessage
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/notify-message/simple-list")
@auth_schema("system:notify-message:query")
async def system_notify_message_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemNotifyMessageDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/notify-message/page")
@auth_schema("system:notify-message:query")
async def system_notify_message_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemNotifyMessageDal(request.state.db)
    search = {**request.query_params}
    
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/notify-message/create")
@auth_schema("system:notify-message:create")
async def system_notify_message_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNotifyMessageDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/notify-message/update")
@auth_schema("system:notify-message:update")
async def system_notify_message_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNotifyMessageDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/notify-message/save")
@auth_schema("system:notify-message:update")
async def system_notify_message_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNotifyMessageDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/notify-message/delete")
@auth_schema("system:notify-message:delete")
async def system_notify_message_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNotifyMessageDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/notify-message/delete-list")
@auth_schema("system:notify-message:delete")
async def system_notify_message_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SystemNotifyMessageDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/notify-message/get")
@auth_schema("system:notify-message:query")
async def system_notify_message_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNotifyMessageDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/notify-message/export-excel")
@auth_schema("system:notify-message:export")
async def system_notify_message_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemNotifyMessageDal(request.state.db)
    await service.ExportExcel(SystemNotifyMessage,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/notify-message/get-unread-count")
async def usystem_notify_message_get_unread_count(request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemNotifyMessageDal(request.state.db)
    data =await dal.GetUnreadCount()
    return Result.success(data)

@router.get("/notify-message/get-unread-list")
async def usystem_notify_message_get_unread_list(request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemNotifyMessageDal(request.state.db)
    data =await dal.GetUnreadList()
    return Result.success(data)
