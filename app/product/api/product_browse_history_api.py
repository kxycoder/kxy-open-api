from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.product.dal.product_browse_history_dal import ProductBrowseHistoryDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.product.models.product_browse_history import ProductBrowseHistory
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/browse-history/simple-list")
@auth_schema("product:browse-history:query")
async def product_browse_history_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = ProductBrowseHistoryDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/browse-history/page")
@auth_schema("product:browse-history:query")
async def product_browse_history_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = ProductBrowseHistoryDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/browse-history/create")
@auth_schema("product:browse-history:create")
async def product_browse_history_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductBrowseHistoryDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/browse-history/update")
@auth_schema("product:browse-history:update")
async def product_browse_history_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductBrowseHistoryDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/browse-history/save")
@auth_schema("product:browse-history:update")
async def product_browse_history_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductBrowseHistoryDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/browse-history/delete")
@auth_schema("product:browse-history:delete")
async def product_browse_history_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductBrowseHistoryDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/browse-history/delete-list")
@auth_schema("product:browse-history:delete")
async def product_browse_history_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = ProductBrowseHistoryDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/browse-history/get")
@auth_schema("product:browse-history:query")
async def product_browse_history_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductBrowseHistoryDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/browse-history/export-excel")
@auth_schema("product:browse-history:export")
async def product_browse_history_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = ProductBrowseHistoryDal(request.state.db)
    await service.ExportExcel(ProductBrowseHistory,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/browse-history/list")
async def uproduct_browse_history_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = ProductBrowseHistoryDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/browse-history/add")
async def uproduct_browse_history_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = ProductBrowseHistoryDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/browse-history/update")
async def uproduct_browse_history_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductBrowseHistoryDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/browse-history/save")
async def uproduct_browse_history_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductBrowseHistoryDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/browse-history/delete")
async def uproduct_browse_history_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductBrowseHistoryDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/browse-history/get")
async def uproduct_browse_history_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductBrowseHistoryDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
