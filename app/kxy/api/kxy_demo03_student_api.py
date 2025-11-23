from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.kxy.dal.kxy_demo03_student_dal import KxyDemo03StudentDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.kxy.models.kxy_demo03_student import KxyDemo03Student
from app.system.services.excel_service import ExcelService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

router = APIRouter()
from app.kxy.dal.kxy_demo03_course_dal import KxyDemo03CourseDal

from app.kxy.dal.kxy_demo03_grade_dal import KxyDemo03GradeDal


@router.get("/demo03-student/simple-list",summary="学生表全部数据",tags=["学生表"])
@auth_schema("kxy:demo03-student:query")
async def kxy_demo03_student_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = KxyDemo03StudentDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/demo03-student/page",summary="学生表分页列表",tags=["学生表"])
@auth_schema("kxy:demo03-student:query")
async def kxy_demo03_student_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = KxyDemo03StudentDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/demo03-student/create",summary="创建学生表",tags=["学生表"])
@auth_schema("kxy:demo03-student:create")
async def kxy_demo03_student_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo03StudentDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)
    demo03CourseList = jsonData.get('demo03CourseList')
    if demo03CourseList:
        await KxyDemo03CourseDal(request.state.db).AddChildrenBatch(data.id,demo03CourseList)
    demo03GradeList = jsonData.get('demo03GradeList')
    if demo03GradeList:
        await KxyDemo03GradeDal(request.state.db).AddChildrenBatch(data.id,demo03GradeList)
    return Result.success(data)

@router.put("/demo03-student/update",summary="更新学生表",tags=["学生表"])
@auth_schema("kxy:demo03-student:update")
async def kxy_demo03_student_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo03StudentDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)
    demo03CourseList = jsonData.get('demo03CourseList')
    if demo03CourseList:
        await KxyDemo03CourseDal(request.state.db).UpdateChildrenBatch(data.id,demo03CourseList)
    demo03GradeList = jsonData.get('demo03GradeList')
    if demo03GradeList:
        await KxyDemo03GradeDal(request.state.db).UpdateChildrenBatch(data.id,demo03GradeList)
    return Result.success(data)


@router.post("/demo03-student/save",summary="新增或更新学生表",tags=["学生表"])
@auth_schema("kxy:demo03-student:update")
async def kxy_demo03_student_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo03StudentDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/demo03-student/delete",summary="删除单个学生表",tags=["学生表"])
@auth_schema("kxy:demo03-student:delete")
async def kxy_demo03_student_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo03StudentDal(request.state.db)
    await KxyDemo03CourseDal(request.state.db).DeleteByParentId(id)
    await KxyDemo03GradeDal(request.state.db).DeleteByParentId(id)
    await dal.Delete(id)
    return Result.success("删除成功")

@router.delete("/demo03-student/delete-list",summary="删除学生表列表",tags=["学生表"])
@auth_schema("kxy:demo03-student:delete")
async def kxy_demo03_student_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = KxyDemo03StudentDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/demo03-student/get",summary="获取单个学生表",tags=["学生表"])
@auth_schema("kxy:demo03-student:query")
async def kxy_demo03_student_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = KxyDemo03StudentDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/demo03-student/export-excel",summary="导出学生表Excel",tags=["学生表"])
@auth_schema("kxy:demo03-student:export")
async def kxy_demo03_student_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = KxyDemo03StudentDal(request.state.db)
    await service.ExportExcel(KxyDemo03Student,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")
