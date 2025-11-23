from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.trade.dal.trade_delivery_express_template_charge_dal import TradeDeliveryExpressTemplateChargeDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.trade.models.trade_delivery_express_template_charge import TradeDeliveryExpressTemplateCharge
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/delivery-express-template-charge/simple-list")
@auth_schema("trade:delivery-express-template-charge:query")
async def trade_delivery_express_template_charge_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/delivery-express-template-charge/page")
@auth_schema("trade:delivery-express-template-charge:query")
async def trade_delivery_express_template_charge_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/delivery-express-template-charge/create")
@auth_schema("trade:delivery-express-template-charge:create")
async def trade_delivery_express_template_charge_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/delivery-express-template-charge/update")
@auth_schema("trade:delivery-express-template-charge:update")
async def trade_delivery_express_template_charge_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/delivery-express-template-charge/save")
@auth_schema("trade:delivery-express-template-charge:update")
async def trade_delivery_express_template_charge_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/delivery-express-template-charge/delete")
@auth_schema("trade:delivery-express-template-charge:delete")
async def trade_delivery_express_template_charge_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/delivery-express-template-charge/delete-list")
@auth_schema("trade:delivery-express-template-charge:delete")
async def trade_delivery_express_template_charge_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/delivery-express-template-charge/get")
@auth_schema("trade:delivery-express-template-charge:query")
async def trade_delivery_express_template_charge_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/delivery-express-template-charge/export-excel")
@auth_schema("trade:delivery-express-template-charge:export")
async def trade_delivery_express_template_charge_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    await service.ExportExcel(TradeDeliveryExpressTemplateCharge,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/delivery-express-template-charge/list")
async def utrade_delivery_express_template_charge_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/delivery-express-template-charge/add")
async def utrade_delivery_express_template_charge_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/delivery-express-template-charge/update")
async def utrade_delivery_express_template_charge_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/delivery-express-template-charge/save")
async def utrade_delivery_express_template_charge_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/delivery-express-template-charge/delete")
async def utrade_delivery_express_template_charge_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/delivery-express-template-charge/get")
async def utrade_delivery_express_template_charge_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeDeliveryExpressTemplateChargeDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
