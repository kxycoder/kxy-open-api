from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.pay.dal.pay_wallet_recharge_dal import PayWalletRechargeDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.pay.models.pay_wallet_recharge import PayWalletRecharge
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/wallet-recharge/simple-list")
@auth_schema("pay:wallet-recharge:query")
async def pay_wallet_recharge_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayWalletRechargeDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/wallet-recharge/page")
@auth_schema("pay:wallet-recharge:query")
async def pay_wallet_recharge_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayWalletRechargeDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/wallet-recharge/create")
@auth_schema("pay:wallet-recharge:create")
async def pay_wallet_recharge_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayWalletRechargeDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/wallet-recharge/update")
@auth_schema("pay:wallet-recharge:update")
async def pay_wallet_recharge_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayWalletRechargeDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/wallet-recharge/save")
@auth_schema("pay:wallet-recharge:update")
async def pay_wallet_recharge_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayWalletRechargeDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/wallet-recharge/delete")
@auth_schema("pay:wallet-recharge:delete")
async def pay_wallet_recharge_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayWalletRechargeDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/wallet-recharge/delete-list")
@auth_schema("pay:wallet-recharge:delete")
async def pay_wallet_recharge_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = PayWalletRechargeDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/wallet-recharge/get")
@auth_schema("pay:wallet-recharge:query")
async def pay_wallet_recharge_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayWalletRechargeDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/wallet-recharge/export-excel")
@auth_schema("pay:wallet-recharge:export")
async def pay_wallet_recharge_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = PayWalletRechargeDal(request.state.db)
    await service.ExportExcel(PayWalletRecharge,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/wallet-recharge/list")
async def upay_wallet_recharge_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = PayWalletRechargeDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/wallet-recharge/add")
async def upay_wallet_recharge_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = PayWalletRechargeDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/wallet-recharge/update")
async def upay_wallet_recharge_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayWalletRechargeDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/wallet-recharge/save")
async def upay_wallet_recharge_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayWalletRechargeDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/wallet-recharge/delete")
async def upay_wallet_recharge_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayWalletRechargeDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/wallet-recharge/get")
async def upay_wallet_recharge_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayWalletRechargeDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
