from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.kxy.dal.kxy_demo03_grade_dal import KxyDemo03GradeDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.kxy.models.kxy_demo03_grade import KxyDemo03Grade
from app.system.services.excel_service import ExcelService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

router = APIRouter()

@router.get("/demo03-grade/simple-list",summary="学生班级表全部数据",tags=["学生班级表"])
@auth_schema("kxy:demo03-grade:query")
async def kxy_demo03_grade_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = KxyDemo03GradeDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/demo03-grade/page",summary="学生班级表分页列表",tags=["学生班级表"])
@auth_schema("kxy:demo03-grade:query")
async def kxy_demo03_grade_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = KxyDemo03GradeDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/demo03-grade/create",summary="创建学生班级表",tags=["学生班级表"])
@auth_schema("kxy:demo03-grade:create")
async def kxy_demo03_grade_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo03GradeDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.put("/demo03-grade/update",summary="更新学生班级表",tags=["学生班级表"])
@auth_schema("kxy:demo03-grade:update")
async def kxy_demo03_grade_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo03GradeDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)
    return Result.success(data)


@router.post("/demo03-grade/save",summary="新增或更新学生班级表",tags=["学生班级表"])
@auth_schema("kxy:demo03-grade:update")
async def kxy_demo03_grade_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo03GradeDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/demo03-grade/delete",summary="删除单个学生班级表",tags=["学生班级表"])
@auth_schema("kxy:demo03-grade:delete")
async def kxy_demo03_grade_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo03GradeDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")

@router.get("/demo03-grade/list-by-student-id",summary="根据父表查询学生班级表列表",tags=["学生班级表"])
@auth_schema("kxy:demo03-grade:query")
async def kxy_demo03_grade_list_by_student_id(request: Request, studentId:int,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo03GradeDal(request.state.db)
    return await dal.GetListByParentId(studentId)

@router.delete("/demo03-grade/delete-list",summary="删除学生班级表列表",tags=["学生班级表"])
@auth_schema("kxy:demo03-grade:delete")
async def kxy_demo03_grade_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = KxyDemo03GradeDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/demo03-grade/get",summary="获取单个学生班级表",tags=["学生班级表"])
@auth_schema("kxy:demo03-grade:query")
async def kxy_demo03_grade_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo03GradeDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/demo03-grade/export-excel",summary="导出学生班级表Excel",tags=["学生班级表"])
@auth_schema("kxy:demo03-grade:export")
async def kxy_demo03_grade_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = KxyDemo03GradeDal(request.state.db)
    await service.ExportExcel(KxyDemo03Grade,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")
