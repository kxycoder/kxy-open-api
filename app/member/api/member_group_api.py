from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.member.dal.member_group_dal import MemberGroupDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.member.models.member_group import MemberGroup
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/group/simple-list")
@auth_schema("member:group:query")
async def member_group_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = MemberGroupDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/group/page")
@auth_schema("member:group:query")
async def member_group_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = MemberGroupDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/group/create")
@auth_schema("member:group:create")
async def member_group_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberGroupDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/group/update")
@auth_schema("member:group:update")
async def member_group_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberGroupDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/group/save")
@auth_schema("member:group:update")
async def member_group_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberGroupDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/group/delete")
@auth_schema("member:group:delete")
async def member_group_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberGroupDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/group/delete-list")
@auth_schema("member:group:delete")
async def member_group_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = MemberGroupDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/group/get")
@auth_schema("member:group:query")
async def member_group_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberGroupDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/group/export-excel")
@auth_schema("member:group:export")
async def member_group_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = MemberGroupDal(request.state.db)
    await service.ExportExcel(MemberGroup,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/group/list")
async def umember_group_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = MemberGroupDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/group/add")
async def umember_group_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = MemberGroupDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/group/update")
async def umember_group_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = MemberGroupDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/group/save")
async def umember_group_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = MemberGroupDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('Id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/group/delete")
async def umember_group_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = MemberGroupDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/group/get")
async def umember_group_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = MemberGroupDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
