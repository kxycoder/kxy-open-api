from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.trade.dal.trade_after_sale_dal import TradeAfterSaleDal
from app.trade.services.after_sale_service import AfterSaleService
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.trade.models.trade_after_sale import TradeAfterSale
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/after-sale/simple-list")
@auth_schema("trade:after-sale:query")
async def trade_after_sale_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeAfterSaleDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/after-sale/page")
@auth_schema("trade:after-sale:query")
async def trade_after_sale_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeAfterSaleDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/after-sale/create")
@auth_schema("trade:after-sale:create")
async def trade_after_sale_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeAfterSaleDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/after-sale/update")
@auth_schema("trade:after-sale:update")
async def trade_after_sale_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeAfterSaleDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)
    return Result.success(data)

# /order/get-detail
@router.get("/after-sale/get-detail")
@auth_schema("trade:after-sale:query")
async def trade_after_sale_get_detail(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    service = AfterSaleService(request.state.db)
    data = await service.GetAfterSaleDetail(id)
    return Result.success(data)

@router.post("/after-sale/save")
@auth_schema("trade:after-sale:update")
async def trade_after_sale_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeAfterSaleDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/after-sale/delete")
@auth_schema("trade:after-sale:delete")
async def trade_after_sale_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeAfterSaleDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/after-sale/delete-list")
@auth_schema("trade:after-sale:delete")
async def trade_after_sale_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = TradeAfterSaleDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/after-sale/get")
@auth_schema("trade:after-sale:query")
async def trade_after_sale_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeAfterSaleDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/after-sale/export-excel")
@auth_schema("trade:after-sale:export")
async def trade_after_sale_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = TradeAfterSaleDal(request.state.db)
    await service.ExportExcel(TradeAfterSale,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/after-sale/list")
async def utrade_after_sale_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = TradeAfterSaleDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/after-sale/add")
async def utrade_after_sale_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = TradeAfterSaleDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/after-sale/update")
async def utrade_after_sale_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeAfterSaleDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/after-sale/save")
async def utrade_after_sale_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeAfterSaleDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/after-sale/delete")
async def utrade_after_sale_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeAfterSaleDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/after-sale/get")
async def utrade_after_sale_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeAfterSaleDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
