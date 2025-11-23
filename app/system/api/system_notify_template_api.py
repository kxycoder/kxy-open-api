from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.contract.types.user_vo import VoSendNotify
from app.system.dal.system_notify_template_dal import SystemNotifyTemplateDal
from app.common.filter import auth_module, auth_schema, get_current_user, get_admin_user
from app.system.models.system_notify_template import SystemNotifyTemplate
from app.system.services.excel_service import ExcelService
router = APIRouter()
from app.system.services.notice_service import NoticeService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/notify-template/simple-list")
@auth_schema("system:notify-template:query")
async def system_notify_template_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemNotifyTemplateDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/notify-template/page")
@auth_schema("system:notify-template:query")
async def system_notify_template_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemNotifyTemplateDal(request.state.db)
    search = {**request.query_params}
    
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/notify-template/create")
@auth_schema("system:notify-template:create")
async def system_notify_template_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNotifyTemplateDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/notify-template/update")
@auth_schema("system:notify-template:update")
async def system_notify_template_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNotifyTemplateDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/notify-template/save")
@auth_schema("system:notify-template:update")
async def system_notify_template_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNotifyTemplateDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/notify-template/delete")
@auth_schema("system:notify-template:delete")
async def system_notify_template_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNotifyTemplateDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/notify-template/delete-list")
@auth_schema("system:notify-template:delete")
async def system_notify_template_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SystemNotifyTemplateDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/notify-template/get")
@auth_schema("system:notify-template:query")
async def system_notify_template_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemNotifyTemplateDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/notify-template/export-excel")
@auth_schema("system:notify-template:export")
async def system_notify_template_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemNotifyTemplateDal(request.state.db)
    await service.ExportExcel(SystemNotifyTemplate,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.post("/notify-template/send-notify")
@auth_schema("system:notify-template:send-notify")
async def system_notify_template_send_notify(data:VoSendNotify,request: Request,current_user: str = Depends(get_admin_user)):
    # {"content":"{code}胜多负少答复收到","params":["code"],"mobile":"","templateCode":"test1","templateParams":{"code":"胜多负少答复收到"},"userType":2,"userId":112}
    svc = NoticeService(request.state.db)
    await svc.SendNotifyMessage(data.userId,data.userType,data.templateCode,**data.templateParams)
    return Result.success(True)