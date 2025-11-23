from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_mail_account_dal import SystemMailAccountDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_mail_account import SystemMailAccount
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/mail-account/simple-list")
@auth_schema("system:mail-account:query")
async def system_mail_account_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemMailAccountDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/mail-account/page")
@auth_schema("system:mail-account:query")
async def system_mail_account_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemMailAccountDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/mail-account/create")
@auth_schema("system:mail-account:create")
async def system_mail_account_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemMailAccountDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/mail-account/update")
@auth_schema("system:mail-account:update")
async def system_mail_account_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemMailAccountDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/mail-account/save")
@auth_schema("system:mail-account:update")
async def system_mail_account_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemMailAccountDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/mail-account/delete")
@auth_schema("system:mail-account:delete")
async def system_mail_account_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemMailAccountDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/mail-account/delete-list")
@auth_schema("system:mail-account:delete")
async def system_mail_account_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = SystemMailAccountDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/mail-account/get")
@auth_schema("system:mail-account:query")
async def system_mail_account_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemMailAccountDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/mail-account/export-excel")
@auth_schema("system:mail-account:export")
async def system_mail_account_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemMailAccountDal(request.state.db)
    await service.ExportExcel(SystemMailAccount,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/u/mail-account/list")
async def usystem_mail_account_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = SystemMailAccountDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/mail-account/add")
async def usystem_mail_account_add(request: Request,current_user: str = Depends(get_current_user)):

    dal = SystemMailAccountDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)

@router.put("/u/mail-account/update")
async def usystem_mail_account_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemMailAccountDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)

@router.post("/u/mail-account/save")
async def usystem_mail_account_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemMailAccountDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)

@router.delete("/u/mail-account/delete")
async def usystem_mail_account_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemMailAccountDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/mail-account/get")
async def usystem_mail_account_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemMailAccountDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)