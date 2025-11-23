from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.trade.dal.trade_config_dal import TradeConfigDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.trade.models.trade_config import TradeConfig
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/config/simple-list")
@auth_schema("trade:config:query")
async def trade_config_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeConfigDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/config/page")
@auth_schema("trade:config:query")
async def trade_config_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = TradeConfigDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/config/create")
@auth_schema("trade:config:create")
async def trade_config_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeConfigDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/config/update")
@auth_schema("trade:config:update")
async def trade_config_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeConfigDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.put("/config/save")
@auth_schema("trade:config:update")
async def trade_config_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeConfigDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/config/delete")
@auth_schema("trade:config:delete")
async def trade_config_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeConfigDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/config/delete-list")
@auth_schema("trade:config:delete")
async def trade_config_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = TradeConfigDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/config/get")
@auth_schema("trade:config:query")
async def trade_config_get(request: Request,current_user: str = Depends(get_admin_user)):
    dal = TradeConfigDal(request.state.db)
    data =await dal.QueryOne([TradeConfig.deleted==0])
    return Result.success(data)


@router.get("/config/export-excel")
@auth_schema("trade:config:export")
async def trade_config_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = TradeConfigDal(request.state.db)
    await service.ExportExcel(TradeConfig,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/config/list")
async def utrade_config_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = TradeConfigDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/config/add")
async def utrade_config_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = TradeConfigDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/config/update")
async def utrade_config_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeConfigDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/config/save")
async def utrade_config_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeConfigDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/config/delete")
async def utrade_config_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeConfigDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/config/get")
async def utrade_config_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = TradeConfigDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
