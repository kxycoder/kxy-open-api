from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.trade.dal.trade_brokerage_withdraw_dal import TradeBrokerageWithdrawDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.trade.models.trade_brokerage_withdraw import TradeBrokerageWithdraw
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/brokerage-withdraw/simple-list")
@auth_schema("trade:brokerage-withdraw:query")
async def trade_brokerage_withdraw_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeBrokerageWithdrawDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/brokerage-withdraw/page")
@auth_schema("trade:brokerage-withdraw:query")
async def trade_brokerage_withdraw_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeBrokerageWithdrawDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/brokerage-withdraw/create")
@auth_schema("trade:brokerage-withdraw:create")
async def trade_brokerage_withdraw_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeBrokerageWithdrawDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.put("/brokerage-withdraw/update")
@auth_schema("trade:brokerage-withdraw:update")
async def trade_brokerage_withdraw_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeBrokerageWithdrawDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)
    return Result.success(data)

@router.post("/brokerage-withdraw/save")
@auth_schema("trade:brokerage-withdraw:update")
async def trade_brokerage_withdraw_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeBrokerageWithdrawDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/brokerage-withdraw/delete")
@auth_schema("trade:brokerage-withdraw:delete")
async def trade_brokerage_withdraw_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeBrokerageWithdrawDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")
    
@router.delete("/brokerage-withdraw/delete-list")
@auth_schema("trade:brokerage-withdraw:delete")
async def trade_brokerage_withdraw_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = TradeBrokerageWithdrawDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')
    
@router.get("/brokerage-withdraw/get")
@auth_schema("trade:brokerage-withdraw:query")
async def trade_brokerage_withdraw_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeBrokerageWithdrawDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/brokerage-withdraw/export-excel")
@auth_schema("trade:brokerage-withdraw:export")
async def trade_brokerage_withdraw_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = TradeBrokerageWithdrawDal(request.state.db)
    await service.ExportExcel(TradeBrokerageWithdraw,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/u/brokerage-withdraw/list")
async def utrade_brokerage_withdraw_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = TradeBrokerageWithdrawDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/brokerage-withdraw/add")
async def utrade_brokerage_withdraw_add(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeBrokerageWithdrawDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)

@router.put("/u/brokerage-withdraw/update")
async def utrade_brokerage_withdraw_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeBrokerageWithdrawDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)

@router.post("/u/brokerage-withdraw/save")
async def utrade_brokerage_withdraw_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeBrokerageWithdrawDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)

@router.delete("/u/brokerage-withdraw/delete")
async def utrade_brokerage_withdraw_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeBrokerageWithdrawDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/brokerage-withdraw/get")
async def utrade_brokerage_withdraw_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeBrokerageWithdrawDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
