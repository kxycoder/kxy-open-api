from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.trade.dal.trade_delivery_express_template_dal import TradeDeliveryExpressTemplateDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.trade.models.trade_delivery_express_template import TradeDeliveryExpressTemplate
from app.system.services.excel_service import ExcelService
from app.trade.services.delivery_service import DeliveryService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/delivery/express-template/simple-list")
@auth_schema("trade:delivery:express-template:query")
async def trade_delivery_express_template_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeDeliveryExpressTemplateDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/delivery/express-template/list-all-simple")
async def trade_delivery_express_template_list_all_simple(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryExpressTemplateDal(request.state.db)
    datas = await dal.GetAllSimpleList()
    return Result.success(datas)

@router.get("/delivery/express-template/page")
@auth_schema("trade:delivery:express-template:query")
async def trade_delivery_express_template_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeDeliveryExpressTemplateDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/delivery/express-template/create")
@auth_schema("trade:delivery:express-template:create")
async def trade_delivery_express_template_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = DeliveryService(request.state.db)
    jsonData = await request.json()
    data = await dal.create_express_template(jsonData)

    return Result.success(data)

@router.put("/delivery/express-template/update")
@auth_schema("trade:delivery:express-template:update")
async def trade_delivery_express_template_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = DeliveryService(request.state.db)
    jsonData = await request.json()
    data = await dal.update_express_template(jsonData.get('id'),jsonData)

    return Result.success(data)


@router.post("/delivery/express-template/save")
@auth_schema("trade:delivery:express-template:update")
async def trade_delivery_express_template_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryExpressTemplateDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/delivery/express-template/delete")
@auth_schema("trade:delivery:express-template:delete")
async def trade_delivery_express_template_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = DeliveryService(request.state.db)
    await dal.delete_express_template(id)
    return Result.success("删除成功")


    
@router.delete("/delivery/express-template/delete-list")
@auth_schema("trade:delivery:express-template:delete")
async def trade_delivery_express_template_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = TradeDeliveryExpressTemplateDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/delivery/express-template/get")
@auth_schema("trade:delivery:express-template:query")
async def trade_delivery_express_template_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    service = DeliveryService(request.state.db)
    data = await service.get_express_template_by_id(id)
    return Result.success(data)


@router.get("/delivery/express-template/export-excel")
@auth_schema("trade:delivery:express-template:export")
async def trade_delivery_express_template_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = TradeDeliveryExpressTemplateDal(request.state.db)
    await service.ExportExcel(TradeDeliveryExpressTemplate,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/delivery/express-template/list")
async def utrade_delivery_express_template_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = TradeDeliveryExpressTemplateDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/delivery/express-template/add")
async def utrade_delivery_express_template_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = TradeDeliveryExpressTemplateDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/delivery/express-template/update")
async def utrade_delivery_express_template_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryExpressTemplateDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/delivery/express-template/save")
async def utrade_delivery_express_template_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryExpressTemplateDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/delivery/express-template/delete")
async def utrade_delivery_express_template_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryExpressTemplateDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/delivery/express-template/get")
async def utrade_delivery_express_template_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    service = DeliveryService(request.state.db)
    data = await service.get_express_template_by_id(id)
    return Result.success(data)
