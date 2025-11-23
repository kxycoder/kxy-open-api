from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.pay.dal.pay_demo_withdraw_dal import PayDemoWithdrawDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.pay.models.pay_demo_withdraw import PayDemoWithdraw
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/demo-withdraw/simple-list")
@auth_schema("pay:demo-withdraw:query")
async def pay_demo_withdraw_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayDemoWithdrawDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/demo-withdraw/page")
@auth_schema("pay:demo-withdraw:query")
async def pay_demo_withdraw_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayDemoWithdrawDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/demo-withdraw/create")
@auth_schema("pay:demo-withdraw:create")
async def pay_demo_withdraw_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayDemoWithdrawDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/demo-withdraw/update")
@auth_schema("pay:demo-withdraw:update")
async def pay_demo_withdraw_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayDemoWithdrawDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/demo-withdraw/save")
@auth_schema("pay:demo-withdraw:update")
async def pay_demo_withdraw_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayDemoWithdrawDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/demo-withdraw/delete")
@auth_schema("pay:demo-withdraw:delete")
async def pay_demo_withdraw_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayDemoWithdrawDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/demo-withdraw/delete-list")
@auth_schema("pay:demo-withdraw:delete")
async def pay_demo_withdraw_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = PayDemoWithdrawDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/demo-withdraw/get")
@auth_schema("pay:demo-withdraw:query")
async def pay_demo_withdraw_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayDemoWithdrawDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/demo-withdraw/export-excel")
@auth_schema("pay:demo-withdraw:export")
async def pay_demo_withdraw_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = PayDemoWithdrawDal(request.state.db)
    await service.ExportExcel(PayDemoWithdraw,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/demo-withdraw/list")
async def upay_demo_withdraw_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = PayDemoWithdrawDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/demo-withdraw/add")
async def upay_demo_withdraw_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = PayDemoWithdrawDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/demo-withdraw/update")
async def upay_demo_withdraw_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayDemoWithdrawDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/demo-withdraw/save")
async def upay_demo_withdraw_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayDemoWithdrawDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/demo-withdraw/delete")
async def upay_demo_withdraw_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayDemoWithdrawDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/demo-withdraw/get")
async def upay_demo_withdraw_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayDemoWithdrawDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
