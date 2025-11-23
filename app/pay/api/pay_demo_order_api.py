from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.pay.dal.pay_demo_order_dal import PayDemoOrderDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.pay.models.pay_demo_order import PayDemoOrder
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/demo-order/simple-list")
@auth_schema("pay:demo-order:query")
async def pay_demo_order_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayDemoOrderDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/demo-order/page")
@auth_schema("pay:demo-order:query")
async def pay_demo_order_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayDemoOrderDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/demo-order/create")
@auth_schema("pay:demo-order:create")
async def pay_demo_order_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayDemoOrderDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/demo-order/update")
@auth_schema("pay:demo-order:update")
async def pay_demo_order_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayDemoOrderDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/demo-order/save")
@auth_schema("pay:demo-order:update")
async def pay_demo_order_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayDemoOrderDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/demo-order/delete")
@auth_schema("pay:demo-order:delete")
async def pay_demo_order_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayDemoOrderDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/demo-order/delete-list")
@auth_schema("pay:demo-order:delete")
async def pay_demo_order_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = PayDemoOrderDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/demo-order/get")
@auth_schema("pay:demo-order:query")
async def pay_demo_order_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayDemoOrderDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/demo-order/export-excel")
@auth_schema("pay:demo-order:export")
async def pay_demo_order_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = PayDemoOrderDal(request.state.db)
    await service.ExportExcel(PayDemoOrder,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/demo-order/list")
async def upay_demo_order_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = PayDemoOrderDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/demo-order/add")
async def upay_demo_order_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = PayDemoOrderDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/demo-order/update")
async def upay_demo_order_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayDemoOrderDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/demo-order/save")
async def upay_demo_order_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayDemoOrderDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/demo-order/delete")
async def upay_demo_order_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayDemoOrderDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/demo-order/get")
async def upay_demo_order_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayDemoOrderDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
