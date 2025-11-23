from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.trade.dal.trade_delivery_express_dal import TradeDeliveryExpressDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.trade.models.trade_delivery_express import TradeDeliveryExpress
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/delivery/express/simple-list")
@router.get("/delivery/express/list-all-simple")
@auth_schema("trade:delivery:express:query")
async def trade_delivery_express_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeDeliveryExpressDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/delivery/express/page")
@auth_schema("trade:delivery:express:query")
async def trade_delivery_express_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeDeliveryExpressDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/delivery/express/create")
@auth_schema("trade:delivery:express:create")
async def trade_delivery_express_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryExpressDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/delivery/express/update")
@auth_schema("trade:delivery:express:update")
async def trade_delivery_express_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryExpressDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/delivery/express/save")
@auth_schema("trade:delivery:express:update")
async def trade_delivery_express_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryExpressDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/delivery/express/delete")
@auth_schema("trade:delivery:express:delete")
async def trade_delivery_express_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryExpressDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/delivery/express/delete-list")
@auth_schema("trade:delivery:express:delete")
async def trade_delivery_express_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = TradeDeliveryExpressDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/delivery/express/get")
@auth_schema("trade:delivery:express:query")
async def trade_delivery_express_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryExpressDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/delivery/express/export-excel")
@auth_schema("trade:delivery:express:export")
async def trade_delivery_express_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = TradeDeliveryExpressDal(request.state.db)
    await service.ExportExcel(TradeDeliveryExpress,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/delivery/express/list")
async def utrade_delivery_express_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = TradeDeliveryExpressDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/delivery/express/add")
async def utrade_delivery_express_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = TradeDeliveryExpressDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/delivery/express/update")
async def utrade_delivery_express_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryExpressDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/delivery/express/save")
async def utrade_delivery_express_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryExpressDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/delivery/express/delete")
async def utrade_delivery_express_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryExpressDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/delivery/express/get")
async def utrade_delivery_express_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryExpressDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
