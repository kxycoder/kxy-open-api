from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.trade.dal.trade_order_log_dal import TradeOrderLogDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.trade.models.trade_order_log import TradeOrderLog
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/order-log/simple-list")
@auth_schema("trade:order-log:query")
async def trade_order_log_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeOrderLogDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/order-log/page")
@auth_schema("trade:order-log:query")
async def trade_order_log_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeOrderLogDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/order-log/create")
@auth_schema("trade:order-log:create")
async def trade_order_log_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderLogDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/order-log/update")
@auth_schema("trade:order-log:update")
async def trade_order_log_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderLogDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/order-log/save")
@auth_schema("trade:order-log:update")
async def trade_order_log_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderLogDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/order-log/delete")
@auth_schema("trade:order-log:delete")
async def trade_order_log_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderLogDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/order-log/delete-list")
@auth_schema("trade:order-log:delete")
async def trade_order_log_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = TradeOrderLogDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/order-log/get")
@auth_schema("trade:order-log:query")
async def trade_order_log_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderLogDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/order-log/export-excel")
@auth_schema("trade:order-log:export")
async def trade_order_log_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = TradeOrderLogDal(request.state.db)
    await service.ExportExcel(TradeOrderLog,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/order-log/list")
async def utrade_order_log_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = TradeOrderLogDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/order-log/add")
async def utrade_order_log_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = TradeOrderLogDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/order-log/update")
async def utrade_order_log_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeOrderLogDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/order-log/save")
async def utrade_order_log_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeOrderLogDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/order-log/delete")
async def utrade_order_log_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeOrderLogDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/order-log/get")
async def utrade_order_log_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeOrderLogDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
