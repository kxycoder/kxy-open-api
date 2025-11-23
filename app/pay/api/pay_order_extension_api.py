from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.pay.dal.pay_order_extension_dal import PayOrderExtensionDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.pay.models.pay_order_extension import PayOrderExtension
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/order-extension/simple-list")
@auth_schema("pay:order-extension:query")
async def pay_order_extension_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayOrderExtensionDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/order-extension/page")
@auth_schema("pay:order-extension:query")
async def pay_order_extension_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayOrderExtensionDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/order-extension/create")
@auth_schema("pay:order-extension:create")
async def pay_order_extension_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayOrderExtensionDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/order-extension/update")
@auth_schema("pay:order-extension:update")
async def pay_order_extension_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayOrderExtensionDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/order-extension/save")
@auth_schema("pay:order-extension:update")
async def pay_order_extension_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayOrderExtensionDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/order-extension/delete")
@auth_schema("pay:order-extension:delete")
async def pay_order_extension_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayOrderExtensionDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/order-extension/delete-list")
@auth_schema("pay:order-extension:delete")
async def pay_order_extension_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = PayOrderExtensionDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/order-extension/get")
@auth_schema("pay:order-extension:query")
async def pay_order_extension_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayOrderExtensionDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/order-extension/export-excel")
@auth_schema("pay:order-extension:export")
async def pay_order_extension_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = PayOrderExtensionDal(request.state.db)
    await service.ExportExcel(PayOrderExtension,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/order-extension/list")
async def upay_order_extension_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = PayOrderExtensionDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/order-extension/add")
async def upay_order_extension_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = PayOrderExtensionDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/order-extension/update")
async def upay_order_extension_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayOrderExtensionDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/order-extension/save")
async def upay_order_extension_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayOrderExtensionDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/order-extension/delete")
async def upay_order_extension_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayOrderExtensionDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/order-extension/get")
async def upay_order_extension_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayOrderExtensionDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
