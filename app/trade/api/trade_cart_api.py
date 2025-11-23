from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.trade.dal.trade_cart_dal import TradeCartDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.trade.models.trade_cart import TradeCart
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/cart/simple-list")
@auth_schema("trade:cart:query")
async def trade_cart_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeCartDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/cart/page")
@auth_schema("trade:cart:query")
async def trade_cart_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeCartDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/cart/create")
@auth_schema("trade:cart:create")
async def trade_cart_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeCartDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/cart/update")
@auth_schema("trade:cart:update")
async def trade_cart_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeCartDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/cart/save")
@auth_schema("trade:cart:update")
async def trade_cart_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeCartDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/cart/delete")
@auth_schema("trade:cart:delete")
async def trade_cart_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeCartDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/cart/delete-list")
@auth_schema("trade:cart:delete")
async def trade_cart_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = TradeCartDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/cart/get")
@auth_schema("trade:cart:query")
async def trade_cart_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeCartDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/cart/export-excel")
@auth_schema("trade:cart:export")
async def trade_cart_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = TradeCartDal(request.state.db)
    await service.ExportExcel(TradeCart,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/cart/list")
async def utrade_cart_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = TradeCartDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/cart/add")
async def utrade_cart_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = TradeCartDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/cart/update")
async def utrade_cart_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeCartDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/cart/save")
async def utrade_cart_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeCartDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/cart/delete")
async def utrade_cart_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeCartDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/cart/get")
async def utrade_cart_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeCartDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
