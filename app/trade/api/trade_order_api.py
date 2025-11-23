from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.trade.dal.trade_order_dal import TradeOrderDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.trade.models.trade_order import TradeOrder
from app.system.services.excel_service import ExcelService
from app.trade.services.order_service import OrderService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/order/simple-list")
@auth_schema("trade:order:query")
async def trade_order_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeOrderDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)
# /order/summary?pageNo=1&pageSize=10&deliveryType=2&pickUpStoreId=2
@router.get("/order/summary")
@auth_schema("trade:order:query")
async def trade_order_summary(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    service = OrderService(request.state.db)
    search = {**request.query_params}
    return Result.success(await service.GetOrderSummary(search))

@router.get("/order/page")
@auth_schema("trade:order:query")
async def trade_order_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    service = OrderService(request.state.db)
    search = {**request.query_params}
    data,total = await service.GetOrderList(search, PageIndex, PageLimit)
    return Result.pagesuccess(data,total)
# /order/get-detail?id=276
@router.get("/order/get-detail")
@auth_schema("trade:order:query")
async def trade_order_get_detail(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    service = OrderService(request.state.db)
    data = await service.GetOrderDetail(id)
    return Result.success(data)

@router.post("/order/create")
@auth_schema("trade:order:create")
async def trade_order_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/order/update-remark")
@router.put("/order/update")
@auth_schema("trade:order:update")
async def trade_order_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)

# /order/delivery
@router.put("/order/delivery")
@auth_schema("trade:order:update")
async def trade_order_delivery(request: Request,current_user: str = Depends(get_admin_user)):
    # {"id":276,"logisticsId":3,"logisticsNo":"sdfsdfsdf"}
    jsonData = await request.json()

    # 校验必填参数
    order_id = jsonData.get('id')
    logistics_id = jsonData.get('logisticsId')
    logistics_no = jsonData.get('logisticsNo')

    if not order_id:
        raise FriendlyException('订单ID不能为空')
    if not logistics_id:
        raise FriendlyException('物流公司不能为空')
    if not logistics_no:
        raise FriendlyException('物流单号不能为空')

    # 调用服务层处理发货逻辑
    service = OrderService(request.state.db)
    order = await service.DeliveryOrder(order_id, logistics_id, logistics_no, current_user)

    return Result.success(order)
@router.post("/order/save")
@auth_schema("trade:order:update")
async def trade_order_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/order/delete")
@auth_schema("trade:order:delete")
async def trade_order_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/order/delete-list")
@auth_schema("trade:order:delete")
async def trade_order_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = TradeOrderDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/order/get")
@auth_schema("trade:order:query")
async def trade_order_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeOrderDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/order/export-excel")
@auth_schema("trade:order:export")
async def trade_order_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = TradeOrderDal(request.state.db)
    await service.ExportExcel(TradeOrder,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/order/list")
async def utrade_order_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = TradeOrderDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/order/add")
async def utrade_order_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = TradeOrderDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/order/update")
async def utrade_order_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeOrderDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/order/save")
async def utrade_order_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeOrderDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/order/delete")
async def utrade_order_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeOrderDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/order/get")
async def utrade_order_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeOrderDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
