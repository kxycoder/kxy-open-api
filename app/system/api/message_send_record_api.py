from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.message_send_record_dal import MessageSendRecordDal
from app.common.filter import auth_module, get_current_user, get_admin_user
from app.system.models.message_send_record import MessageSendRecord
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/message_send_record/list")
@auth_module(module_name="message_send_record", resource="list")
async def message_send_record_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = MessageSendRecordDal(request.state.db)
    search = {**request.query_params}
    
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/message_send_record/add")
@auth_module(module_name="message_send_record", resource="add")
async def message_send_record_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MessageSendRecordDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.post("/message_send_record/update")
@auth_module(module_name="message_send_record", resource="update")
async def message_send_record_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MessageSendRecordDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/message_send_record/save")
async def message_send_record_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = MessageSendRecordDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.get("/message_send_record/delete")
@auth_module(module_name="message_send_record", resource="delete")
async def message_send_record_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = MessageSendRecordDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.post("/message_send_record/deletebatch")
@auth_module(module_name="message_send_record", resource="delete")
async def message_send_record_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = MessageSendRecordDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/message_send_record/get")
@auth_module(module_name="message_send_record", resource="get")
async def message_send_record_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = MessageSendRecordDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/message_send_record/export_excel")
@auth_module(module_name="message_send_record", resource="export_excel")
async def message_send_record_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = MessageSendRecordDal(request.state.db)
    await service.ExportExcel(MessageSendRecord,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")