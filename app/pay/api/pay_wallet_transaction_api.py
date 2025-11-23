from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.pay.dal.pay_wallet_transaction_dal import PayWalletTransactionDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.pay.models.pay_wallet_transaction import PayWalletTransaction
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/wallet-transaction/simple-list")
@auth_schema("pay:wallet-transaction:query")
async def pay_wallet_transaction_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayWalletTransactionDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/wallet-transaction/page")
@auth_schema("pay:wallet-transaction:query")
async def pay_wallet_transaction_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayWalletTransactionDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/wallet-transaction/create")
@auth_schema("pay:wallet-transaction:create")
async def pay_wallet_transaction_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayWalletTransactionDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/wallet-transaction/update")
@auth_schema("pay:wallet-transaction:update")
async def pay_wallet_transaction_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayWalletTransactionDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/wallet-transaction/save")
@auth_schema("pay:wallet-transaction:update")
async def pay_wallet_transaction_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayWalletTransactionDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/wallet-transaction/delete")
@auth_schema("pay:wallet-transaction:delete")
async def pay_wallet_transaction_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayWalletTransactionDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/wallet-transaction/delete-list")
@auth_schema("pay:wallet-transaction:delete")
async def pay_wallet_transaction_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = PayWalletTransactionDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/wallet-transaction/get")
@auth_schema("pay:wallet-transaction:query")
async def pay_wallet_transaction_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayWalletTransactionDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/wallet-transaction/export-excel")
@auth_schema("pay:wallet-transaction:export")
async def pay_wallet_transaction_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = PayWalletTransactionDal(request.state.db)
    await service.ExportExcel(PayWalletTransaction,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/wallet-transaction/list")
async def upay_wallet_transaction_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = PayWalletTransactionDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/wallet-transaction/add")
async def upay_wallet_transaction_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = PayWalletTransactionDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/wallet-transaction/update")
async def upay_wallet_transaction_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayWalletTransactionDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/wallet-transaction/save")
async def upay_wallet_transaction_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayWalletTransactionDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/wallet-transaction/delete")
async def upay_wallet_transaction_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayWalletTransactionDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/wallet-transaction/get")
async def upay_wallet_transaction_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayWalletTransactionDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
