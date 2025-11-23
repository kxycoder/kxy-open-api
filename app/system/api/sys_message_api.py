from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.sys_message_dal import SysMessageDal
from app.common.filter import auth_module, get_current_user, tryCatch, get_admin_user
from app.system.models.sys_message import SysMessage
from app.system.services.excel_service import ExcelService
router = APIRouter()
from app.system.services.message_service import MessageService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/sys_message/list")
@auth_module(module_name="sys_message", resource="list")
async def sys_message_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = SysMessageDal(request.state.db)
    data,total =await dal.Search(request.query_params,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)
@router.post("/sys_message/add")
@auth_module(module_name="sys_message", resource="add")
async def sys_message_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysMessageDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.post("/sys_message/update")
@auth_module(module_name="sys_message", resource="update")
async def sys_message_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysMessageDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/sys_message/save")
async def sys_message_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysMessageDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.get("/sys_message/delete")
@auth_module(module_name="sys_message", resource="delete")
async def sys_message_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysMessageDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.post("/sys_message/deletebatch")
@auth_module(module_name="sys_message", resource="delete")
async def sys_message_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SysMessageDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/sys_message/get")
@auth_module(module_name="sys_message", resource="get")
async def sys_message_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysMessageDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/sys_message/export_excel")
@auth_module(module_name="sys_message", resource="export_excel")
async def sys_message_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SysMessageDal(request.state.db)
    await service.ExportExcel(SysMessage,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/u/sys_message/list")
async def usys_message_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = SysMessageDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit)
    return Result.pagesuccess(datas,total)

@router.get("/messages")
async def usys_message_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("page", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = SysMessageDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit)
    datas = [d.to_mini_dict() for d in datas]
    return Result.pagesuccess(datas,total)
# read-batch
@router.post("/messages/read-batch")
async def usys_message_read_batch(request: Request,current_user: str = Depends(get_current_user)):
    jsonData = await request.json()
    messageIds=jsonData.get('messageIds')
    if messageIds:
        dal = MessageService(request.state.db)
        await dal.ReadMsgBatch(messageIds)
    return Result.success("ok")
    
    
# @router.post("/u/sys_message/add")
# async def usys_message_add(request: Request,current_user: str = Depends(get_current_user)):

#     dal = SysMessageDal(request.state.db)
#     data =await dal.AddByJsonDataUser(await request.json())
#     return Result.success(data)

# @router.post("/u/sys_message/update")
# async def usys_message_update(request: Request,current_user: str = Depends(get_current_user)):
#     dal = SysMessageDal(request.state.db)
#     data =await dal.UpdateByJsonDataUser(await request.json())
#     return Result.success(data)

# @router.post("/u/sys_message/save")
# async def usys_message_save(request: Request,current_user: str = Depends(get_current_user)):
#     dal = SysMessageDal(request.state.db)
#     jsonData = await request.json()
#     if jsonData.get('id'):
#         data =await dal.UpdateByJsonDataUser(jsonData)
#     else:
#         data =await dal.AddByJsonDataUser(jsonData)
#     return Result.success(data)

# @router.get("/u/sys_message/delete")
# async def usys_message_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
#     dal = SysMessageDal(request.state.db)
#     data =await dal.DeleteByUser(id)
#     return Result.success("删除成功")
        
# @router.get("/u/sys_message/get")
# async def usys_message_get(id:str,request: Request,current_user: str = Depends(get_current_user)):
#     dal = SysMessageDal(request.state.db)
#     data =await dal.GetExistByUser(id)
#     return Result.success(data)