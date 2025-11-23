from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.trade.dal.trade_delivery_pick_up_store_dal import TradeDeliveryPickUpStoreDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.trade.models.trade_delivery_pick_up_store import TradeDeliveryPickUpStore
from app.system.services.excel_service import ExcelService
from app.trade.services.delivery_service import DeliveryService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/delivery/pick-up-store/simple-list")
@auth_schema("trade:delivery-pick-up-store:query")
async def trade_delivery_pick_up_store_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeDeliveryPickUpStoreDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/delivery/pick-up-store/page")
@auth_schema("trade:delivery-pick-up-store:query")
async def trade_delivery_pick_up_store_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeDeliveryPickUpStoreDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/delivery/pick-up-store/create")
@auth_schema("trade:delivery-pick-up-store:create")
async def trade_delivery_pick_up_store_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryPickUpStoreDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)
    return Result.success(data)

# /delivery/pick-up-store/bind
@router.post("/delivery/pick-up-store/bind")
@auth_schema("trade:delivery-pick-up-store:update")
async def trade_delivery_pick_up_store_bind(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    verifyUserIds = jsonData.get('verifyUserIds', [])
    id = jsonData.get('id')
    service = DeliveryService(request.state.db)
    data = await service.bind_verify_users(id, verifyUserIds)
    return Result.success(data)

@router.put("/delivery/pick-up-store/update")
@auth_schema("trade:delivery-pick-up-store:update")
async def trade_delivery_pick_up_store_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryPickUpStoreDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)
    return Result.success(data)

@router.post("/delivery/pick-up-store/save")
@auth_schema("trade:delivery-pick-up-store:update")
async def trade_delivery_pick_up_store_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryPickUpStoreDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/delivery/pick-up-store/delete")
@auth_schema("trade:delivery-pick-up-store:delete")
async def trade_delivery_pick_up_store_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryPickUpStoreDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")
    
@router.delete("/delivery/pick-up-store/delete-list")
@auth_schema("trade:delivery-pick-up-store:delete")
async def trade_delivery_pick_up_store_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = TradeDeliveryPickUpStoreDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/delivery/pick-up-store/get")
@auth_schema("trade:delivery-pick-up-store:query")
async def trade_delivery_pick_up_store_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = DeliveryService(request.state.db)
    data =await dal.get_store(id)
    return Result.success(data)

@router.get("/delivery/pick-up-store/export-excel")
@auth_schema("trade:delivery-pick-up-store:export")
async def trade_delivery_pick_up_store_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = TradeDeliveryPickUpStoreDal(request.state.db)
    await service.ExportExcel(TradeDeliveryPickUpStore,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

@router.get("/u/delivery/pick-up-store/list")
async def utrade_delivery_pick_up_store_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = TradeDeliveryPickUpStoreDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/delivery/pick-up-store/add")
async def utrade_delivery_pick_up_store_add(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryPickUpStoreDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)

@router.put("/u/delivery/pick-up-store/update")
async def utrade_delivery_pick_up_store_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryPickUpStoreDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)

@router.post("/u/delivery/pick-up-store/save")
async def utrade_delivery_pick_up_store_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryPickUpStoreDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)

@router.delete("/u/delivery/pick-up-store/delete")
async def utrade_delivery_pick_up_store_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryPickUpStoreDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/delivery/pick-up-store/get")
async def utrade_delivery_pick_up_store_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryPickUpStoreDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
