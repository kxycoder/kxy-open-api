from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.product.dal.product_spu_dal import ProductSpuDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.product.models.product_spu import ProductSpu
from app.product.services.product_service import ProductService
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/spu/simple-list")
@auth_schema("product:spu:query")
async def product_spu_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = ProductSpuDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/spu/page")
@auth_schema("product:spu:query")
async def product_spu_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = ProductSpuDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/spu/create")
@auth_schema("product:spu:create")
async def product_spu_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductSpuDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.put("/spu/update")
@auth_schema("product:spu:update")
async def product_spu_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductService(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)
    return Result.success(data)

@router.post("/spu/save")
@auth_schema("product:spu:update")
async def product_spu_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductSpuDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/spu/delete")
@auth_schema("product:spu:delete")
async def product_spu_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductSpuDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")
    
@router.delete("/spu/delete-list")
@auth_schema("product:spu:delete")
async def product_spu_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = ProductSpuDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/spu/get")
@auth_schema("product:spu:query")
async def product_spu_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductSpuDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/spu/export-excel")
@auth_schema("product:spu:export")
async def product_spu_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = ProductSpuDal(request.state.db)
    await service.ExportExcel(ProductSpu,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")
# spu/get-count
@router.get("/spu/get-count")
async def product_spu_get_count(request: Request,current_user: str = Depends(get_admin_user)):
    # {"code":0,"data":{"0":6,"1":1,"2":1,"3":4,"4":0},"msg":""}
    dal = ProductSpuDal(request.state.db)
    data =await dal.GetCount()
    return Result.success(data)

@router.get("/u/spu/list")
async def uproduct_spu_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = ProductSpuDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/spu/add")
async def uproduct_spu_add(request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductSpuDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)

@router.post("/u/spu/save")
async def uproduct_spu_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductSpuDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)

@router.delete("/u/spu/delete")
async def uproduct_spu_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductSpuDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/spu/get")
async def uproduct_spu_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductSpuDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)

# /spu/get-detail?id=641
@router.get("/spu/get-detail")
async def product_spu_get_detail(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductService(request.state.db)
    data =await dal.GetSpuDetail(id)
    return Result.success(data)