from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.kxy.dal.kxy_demo01_contact_dal import KxyDemo01ContactDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.kxy.models.kxy_demo01_contact import KxyDemo01Contact
from app.system.services.excel_service import ExcelService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

router = APIRouter()

@router.get("/demo01-contact/simple-list",summary="示例联系人表全部数据",tags=["示例联系人表"])
@auth_schema("kxy:demo01-contact:query")
async def kxy_demo01_contact_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = KxyDemo01ContactDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/demo01-contact/page",summary="示例联系人表分页列表",tags=["示例联系人表"])
@auth_schema("kxy:demo01-contact:query")
async def kxy_demo01_contact_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = KxyDemo01ContactDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/demo01-contact/create",summary="创建示例联系人表",tags=["示例联系人表"])
@auth_schema("kxy:demo01-contact:create")
async def kxy_demo01_contact_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo01ContactDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.put("/demo01-contact/update",summary="更新示例联系人表",tags=["示例联系人表"])
@auth_schema("kxy:demo01-contact:update")
async def kxy_demo01_contact_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo01ContactDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)
    return Result.success(data)


@router.post("/demo01-contact/save",summary="新增或更新示例联系人表",tags=["示例联系人表"])
@auth_schema("kxy:demo01-contact:update")
async def kxy_demo01_contact_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo01ContactDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/demo01-contact/delete",summary="删除单个示例联系人表",tags=["示例联系人表"])
@auth_schema("kxy:demo01-contact:delete")
async def kxy_demo01_contact_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo01ContactDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")

@router.delete("/demo01-contact/delete-list",summary="删除示例联系人表列表",tags=["示例联系人表"])
@auth_schema("kxy:demo01-contact:delete")
async def kxy_demo01_contact_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = KxyDemo01ContactDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/demo01-contact/get",summary="获取单个示例联系人表",tags=["示例联系人表"])
@auth_schema("kxy:demo01-contact:query")
async def kxy_demo01_contact_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo01ContactDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/demo01-contact/export-excel",summary="导出示例联系人表Excel",tags=["示例联系人表"])
@auth_schema("kxy:demo01-contact:export")
async def kxy_demo01_contact_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = KxyDemo01ContactDal(request.state.db)
    await service.ExportExcel(KxyDemo01Contact,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")
