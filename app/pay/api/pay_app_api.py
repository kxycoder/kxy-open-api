from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.pay.dal.pay_app_dal import PayAppDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.pay.models.pay_app import PayApp
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/app/simple-list")
@auth_schema("pay:app:query")
async def pay_app_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayAppDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/app/page")
@router.get("/app/list")
@auth_schema("pay:app:query")
async def pay_app_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = PayAppDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/app/create")
@auth_schema("pay:app:create")
async def pay_app_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayAppDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/app/update")
@auth_schema("pay:app:update")
async def pay_app_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayAppDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/app/save")
@auth_schema("pay:app:update")
async def pay_app_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayAppDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/app/delete")
@auth_schema("pay:app:delete")
async def pay_app_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayAppDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/app/delete-list")
@auth_schema("pay:app:delete")
async def pay_app_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = PayAppDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/app/get")
@auth_schema("pay:app:query")
async def pay_app_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = PayAppDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/app/export-excel")
@auth_schema("pay:app:export")
async def pay_app_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = PayAppDal(request.state.db)
    await service.ExportExcel(PayApp,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/app/list")
async def upay_app_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = PayAppDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/app/add")
async def upay_app_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = PayAppDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/app/update")
async def upay_app_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayAppDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/app/save")
async def upay_app_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = PayAppDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/app/delete")
async def upay_app_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayAppDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/app/get")
async def upay_app_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = PayAppDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
