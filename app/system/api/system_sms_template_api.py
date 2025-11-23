from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.contract.types.send_types import SmsTestObject
from app.system.dal.system_sms_template_dal import SystemSmsTemplateDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_sms_template import SystemSmsTemplate
from app.system.services.excel_service import ExcelService
router = APIRouter()
from app.system.services.sms_service import SmsService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/sms-template/simple-list")
@auth_schema("system:sms-template:query")
async def system_sms_template_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemSmsTemplateDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/sms-template/page")
@auth_schema("system:sms-template:query")
async def system_sms_template_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemSmsTemplateDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/sms-template/create")
@auth_schema("system:sms-template:create")
async def system_sms_template_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SmsService(request.state.db)
    data = await dal.AddTemplate(await request.json())
    return Result.success(data)
# sms-template/send-sms
@router.post("/sms-template/send-sms")
@auth_schema("system:sms-template:send-sms")
async def system_sms_template_send_sms(data:SmsTestObject,request: Request,current_user: str = Depends(get_admin_user)):
    # {"content":"您的验证码为：{code}，请勿泄露于他人！","params":["code"],"mobile":"18601650373","templateCode":"login","templateParams":{"code":"456142"}}
    dal = SmsService(request.state.db)
    data = await dal.SendByDetail(current_user,1,data.mobile,data.templateCode,**data.templateParams)
    return Result.success(data)

@router.put("/sms-template/update")
@auth_schema("system:sms-template:update")
async def system_sms_template_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsTemplateDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/sms-template/save")
@auth_schema("system:sms-template:update")
async def system_sms_template_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsTemplateDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/sms-template/delete")
@auth_schema("system:sms-template:delete")
async def system_sms_template_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsTemplateDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/sms-template/delete-list")
@auth_schema("system:sms-template:delete")
async def system_sms_template_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = SystemSmsTemplateDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/sms-template/get")
@auth_schema("system:sms-template:query")
async def system_sms_template_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSmsTemplateDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/sms-template/export-excel")
@auth_schema("system:sms-template:export")
async def system_sms_template_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemSmsTemplateDal(request.state.db)
    await service.ExportExcel(SystemSmsTemplate,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")