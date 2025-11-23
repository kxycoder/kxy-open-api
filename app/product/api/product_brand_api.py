from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.product.dal.product_brand_dal import ProductBrandDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.product.models.product_brand import ProductBrand
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/brand/simple-list")
@auth_schema("product:brand:query")
async def product_brand_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = ProductBrandDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/brand/page")
@auth_schema("product:brand:query")
async def product_brand_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = ProductBrandDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/brand/create")
@auth_schema("product:brand:create")
async def product_brand_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductBrandDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/brand/update")
@auth_schema("product:brand:update")
async def product_brand_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductBrandDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/brand/save")
@auth_schema("product:brand:update")
async def product_brand_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductBrandDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/brand/delete")
@auth_schema("product:brand:delete")
async def product_brand_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductBrandDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/brand/delete-list")
@auth_schema("product:brand:delete")
async def product_brand_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = ProductBrandDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/brand/get")
@auth_schema("product:brand:query")
async def product_brand_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductBrandDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/brand/export-excel")
@auth_schema("product:brand:export")
async def product_brand_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = ProductBrandDal(request.state.db)
    await service.ExportExcel(ProductBrand,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/brand/list")
async def uproduct_brand_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = ProductBrandDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/brand/add")
async def uproduct_brand_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = ProductBrandDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/brand/update")
async def uproduct_brand_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductBrandDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/brand/save")
async def uproduct_brand_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductBrandDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/brand/delete")
async def uproduct_brand_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductBrandDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/brand/get")
async def uproduct_brand_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductBrandDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)

# /brand/list-all-simple
@router.get("/brand/list-all-simple")
@auth_schema("product:brand:query")
async def product_brand_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductBrandDal(request.state.db)
    datas = await dal.GetAllSimpleList()
    return Result.success(datas)