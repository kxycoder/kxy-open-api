from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.pay.dal.pay_notify_log_dal import PayNotifyLogDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.pay.models.pay_notify_log import PayNotifyLog
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/notify/simple-list")
@auth_schema("pay:notify:query")
async def pay_notify_log_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayNotifyLogDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/notify/page")
@auth_schema("pay:notify:query")
async def pay_notify_log_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayNotifyLogDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/notify/create")
@auth_schema("pay:notify:create")
async def pay_notify_log_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayNotifyLogDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/notify/update")
@auth_schema("pay:notify:update")
async def pay_notify_log_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayNotifyLogDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/notify/save")
@auth_schema("pay:notify:update")
async def pay_notify_log_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayNotifyLogDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/notify/delete")
@auth_schema("pay:notify:delete")
async def pay_notify_log_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayNotifyLogDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/notify/delete-list")
@auth_schema("pay:notify:delete")
async def pay_notify_log_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = PayNotifyLogDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/notify/get")
@auth_schema("pay:notify:query")
async def pay_notify_log_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayNotifyLogDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/notify/export-excel")
@auth_schema("pay:notify:export")
async def pay_notify_log_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = PayNotifyLogDal(request.state.db)
    await service.ExportExcel(PayNotifyLog,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/notify/list")
async def upay_notify_log_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = PayNotifyLogDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/notify/add")
async def upay_notify_log_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = PayNotifyLogDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/notify/update")
async def upay_notify_log_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayNotifyLogDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/notify/save")
async def upay_notify_log_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayNotifyLogDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/notify/delete")
async def upay_notify_log_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayNotifyLogDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/notify/get")
async def upay_notify_log_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayNotifyLogDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
