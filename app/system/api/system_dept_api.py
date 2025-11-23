from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.system_dept_dal import SystemDeptDal
from app.common.filter import auth_module, auth_schema, get_current_user, get_admin_user
from app.system.models.system_dept import SystemDept
from app.system.services.excel_service import ExcelService
router = APIRouter()
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/dept/simple-list")
@router.get("/dept/list")
@auth_schema("system:dept:query")
async def system_dept_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemDeptDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/dept/page")
@auth_schema("system:dept:query")
async def system_dept_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemDeptDal(request.state.db)
    search = {**request.query_params}
    
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/dept/create")
@auth_schema("system:dept:create")
async def system_dept_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDeptDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/dept/update")
@auth_schema("system:dept:update")
async def system_dept_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDeptDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/dept/save")
@auth_schema("system:dept:update")
async def system_dept_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDeptDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/dept/delete")
@auth_schema("system:dept:delete")
async def system_dept_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDeptDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/dept/delete-list")
@auth_schema("system:dept:delete")
async def system_dept_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SystemDeptDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/dept/get")
@auth_schema("system:dept:query")
async def system_dept_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemDeptDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/dept/export-excel")
@auth_schema("system:dept:export")
async def system_dept_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemDeptDal(request.state.db)
    await service.ExportExcel(SystemDept,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")
