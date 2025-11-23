from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.trade.dal.trade_order_item_dal import TradeOrderItemDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.trade.models.trade_order_item import TradeOrderItem
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/order-item/simple-list")
@auth_schema("trade:order-item:query")
async def trade_order_item_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeOrderItemDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/order-item/page")
@auth_schema("trade:order-item:query")
async def trade_order_item_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeOrderItemDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/order-item/create")
@auth_schema("trade:order-item:create")
async def trade_order_item_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderItemDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/order-item/update")
@auth_schema("trade:order-item:update")
async def trade_order_item_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderItemDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/order-item/save")
@auth_schema("trade:order-item:update")
async def trade_order_item_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderItemDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/order-item/delete")
@auth_schema("trade:order-item:delete")
async def trade_order_item_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderItemDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/order-item/delete-list")
@auth_schema("trade:order-item:delete")
async def trade_order_item_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = TradeOrderItemDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/order-item/get")
@auth_schema("trade:order-item:query")
async def trade_order_item_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderItemDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/order-item/export-excel")
@auth_schema("trade:order-item:export")
async def trade_order_item_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = TradeOrderItemDal(request.state.db)
    await service.ExportExcel(TradeOrderItem,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/order-item/list")
async def utrade_order_item_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = TradeOrderItemDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/order-item/add")
async def utrade_order_item_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = TradeOrderItemDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/order-item/update")
async def utrade_order_item_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeOrderItemDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/order-item/save")
async def utrade_order_item_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeOrderItemDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/order-item/delete")
async def utrade_order_item_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeOrderItemDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/order-item/get")
async def utrade_order_item_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeOrderItemDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
