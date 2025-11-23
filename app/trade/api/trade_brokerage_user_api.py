from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.trade.dal.trade_brokerage_user_dal import TradeBrokerageUserDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.trade.models.trade_brokerage_user import TradeBrokerageUser
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/brokerage-user/simple-list")
@auth_schema("trade:brokerage-user:query")
async def trade_brokerage_user_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeBrokerageUserDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/brokerage-user/page")
@auth_schema("trade:brokerage-user:query")
async def trade_brokerage_user_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeBrokerageUserDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/brokerage-user/create")
@auth_schema("trade:brokerage-user:create")
async def trade_brokerage_user_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeBrokerageUserDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/brokerage-user/update")
@auth_schema("trade:brokerage-user:update")
async def trade_brokerage_user_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeBrokerageUserDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/brokerage-user/save")
@auth_schema("trade:brokerage-user:update")
async def trade_brokerage_user_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeBrokerageUserDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/brokerage-user/delete")
@auth_schema("trade:brokerage-user:delete")
async def trade_brokerage_user_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeBrokerageUserDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/brokerage-user/delete-list")
@auth_schema("trade:brokerage-user:delete")
async def trade_brokerage_user_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = TradeBrokerageUserDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/brokerage-user/get")
@auth_schema("trade:brokerage-user:query")
async def trade_brokerage_user_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeBrokerageUserDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/brokerage-user/export-excel")
@auth_schema("trade:brokerage-user:export")
async def trade_brokerage_user_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = TradeBrokerageUserDal(request.state.db)
    await service.ExportExcel(TradeBrokerageUser,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/brokerage-user/list")
async def utrade_brokerage_user_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = TradeBrokerageUserDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/brokerage-user/add")
async def utrade_brokerage_user_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = TradeBrokerageUserDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/brokerage-user/update")
async def utrade_brokerage_user_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeBrokerageUserDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/brokerage-user/save")
async def utrade_brokerage_user_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeBrokerageUserDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/brokerage-user/delete")
async def utrade_brokerage_user_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeBrokerageUserDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/brokerage-user/get")
async def utrade_brokerage_user_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeBrokerageUserDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
