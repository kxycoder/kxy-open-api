from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.trade.dal.trade_statistics_dal import TradeStatisticsDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.trade.models.trade_statistics import TradeStatistics
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/statistics/simple-list")
@auth_schema("trade:statistics:query")
async def trade_statistics_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeStatisticsDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/statistics/page")
@auth_schema("trade:statistics:query")
async def trade_statistics_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeStatisticsDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/statistics/create")
@auth_schema("trade:statistics:create")
async def trade_statistics_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeStatisticsDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/statistics/update")
@auth_schema("trade:statistics:update")
async def trade_statistics_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeStatisticsDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/statistics/save")
@auth_schema("trade:statistics:update")
async def trade_statistics_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeStatisticsDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/statistics/delete")
@auth_schema("trade:statistics:delete")
async def trade_statistics_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeStatisticsDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/statistics/delete-list")
@auth_schema("trade:statistics:delete")
async def trade_statistics_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = TradeStatisticsDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/statistics/get")
@auth_schema("trade:statistics:query")
async def trade_statistics_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeStatisticsDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/statistics/export-excel")
@auth_schema("trade:statistics:export")
async def trade_statistics_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = TradeStatisticsDal(request.state.db)
    await service.ExportExcel(TradeStatistics,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/statistics/list")
async def utrade_statistics_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = TradeStatisticsDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/statistics/add")
async def utrade_statistics_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = TradeStatisticsDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/statistics/update")
async def utrade_statistics_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeStatisticsDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/statistics/save")
async def utrade_statistics_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeStatisticsDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/statistics/delete")
async def utrade_statistics_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeStatisticsDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/statistics/get")
async def utrade_statistics_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeStatisticsDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
