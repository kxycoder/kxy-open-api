from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.product.dal.product_property_value_dal import ProductPropertyValueDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.product.models.product_property_value import ProductPropertyValue
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/property/value/simple-list")
@auth_schema("product:property/value:query")
async def product_property_value_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = ProductPropertyValueDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/property/value/page")
@auth_schema("product:property/value:query")
async def product_property_value_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = ProductPropertyValueDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/property/value/create")
@auth_schema("product:property/value:create")
async def product_property_value_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductPropertyValueDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/property/value/update")
@auth_schema("product:property/value:update")
async def product_property_value_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductPropertyValueDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/property/value/save")
@auth_schema("product:property/value:update")
async def product_property_value_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductPropertyValueDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/property/value/delete")
@auth_schema("product:property/value:delete")
async def product_property_value_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductPropertyValueDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/property/value/delete-list")
@auth_schema("product:property/value:delete")
async def product_property_value_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = ProductPropertyValueDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/property/value/get")
@auth_schema("product:property/value:query")
async def product_property_value_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductPropertyValueDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/property/value/export-excel")
@auth_schema("product:property/value:export")
async def product_property_value_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = ProductPropertyValueDal(request.state.db)
    await service.ExportExcel(ProductPropertyValue,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/property/value/list")
async def uproduct_property_value_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = ProductPropertyValueDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/property/value/add")
async def uproduct_property_value_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = ProductPropertyValueDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/property/value/update")
async def uproduct_property_value_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductPropertyValueDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/property/value/save")
async def uproduct_property_value_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductPropertyValueDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/property/value/delete")
async def uproduct_property_value_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductPropertyValueDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/property/value/get")
async def uproduct_property_value_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductPropertyValueDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
