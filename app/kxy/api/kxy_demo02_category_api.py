from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.kxy.dal.kxy_demo02_category_dal import KxyDemo02CategoryDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.kxy.models.kxy_demo02_category import KxyDemo02Category
from app.system.services.excel_service import ExcelService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

router = APIRouter()

@router.get("/demo02-category/simple-list",summary="示例分类表全部数据",tags=["示例分类表"])
@auth_schema("kxy:demo02-category:query")
async def kxy_demo02_category_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = KxyDemo02CategoryDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/demo02-category/page",summary="示例分类表分页列表",tags=["示例分类表"])
@auth_schema("kxy:demo02-category:query")
async def kxy_demo02_category_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = KxyDemo02CategoryDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/demo02-category/create",summary="创建示例分类表",tags=["示例分类表"])
@auth_schema("kxy:demo02-category:create")
async def kxy_demo02_category_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo02CategoryDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.put("/demo02-category/update",summary="更新示例分类表",tags=["示例分类表"])
@auth_schema("kxy:demo02-category:update")
async def kxy_demo02_category_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo02CategoryDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)
    return Result.success(data)


@router.post("/demo02-category/save",summary="新增或更新示例分类表",tags=["示例分类表"])
@auth_schema("kxy:demo02-category:update")
async def kxy_demo02_category_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo02CategoryDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/demo02-category/delete",summary="删除单个示例分类表",tags=["示例分类表"])
@auth_schema("kxy:demo02-category:delete")
async def kxy_demo02_category_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo02CategoryDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")

@router.delete("/demo02-category/delete-list",summary="删除示例分类表列表",tags=["示例分类表"])
@auth_schema("kxy:demo02-category:delete")
async def kxy_demo02_category_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = KxyDemo02CategoryDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/demo02-category/get",summary="获取单个示例分类表",tags=["示例分类表"])
@auth_schema("kxy:demo02-category:query")
async def kxy_demo02_category_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo02CategoryDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/demo02-category/export-excel",summary="导出示例分类表Excel",tags=["示例分类表"])
@auth_schema("kxy:demo02-category:export")
async def kxy_demo02_category_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = KxyDemo02CategoryDal(request.state.db)
    await service.ExportExcel(KxyDemo02Category,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")
