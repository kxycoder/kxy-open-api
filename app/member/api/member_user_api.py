from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.member.dal.member_user_dal import MemberUserDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.member.models.member_user import MemberUser
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/user/simple-list")
@auth_schema("member:user:query")
async def member_user_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = MemberUserDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/user/page")
@auth_schema("member:user:query")
async def member_user_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = MemberUserDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/user/create")
@auth_schema("member:user:create")
async def member_user_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberUserDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/user/update")
@auth_schema("member:user:update")
async def member_user_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberUserDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/user/save")
@auth_schema("member:user:update")
async def member_user_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberUserDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/user/delete")
@auth_schema("member:user:delete")
async def member_user_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberUserDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/user/delete-list")
@auth_schema("member:user:delete")
async def member_user_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = MemberUserDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/user/get")
@auth_schema("member:user:query")
async def member_user_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberUserDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/user/export-excel")
@auth_schema("member:user:export")
async def member_user_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = MemberUserDal(request.state.db)
    await service.ExportExcel(MemberUser,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/user/list")
async def umember_user_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = MemberUserDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/user/add")
async def umember_user_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = MemberUserDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/user/update")
async def umember_user_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = MemberUserDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/user/save")
async def umember_user_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = MemberUserDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('Id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/user/delete")
async def umember_user_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = MemberUserDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/user/get")
async def umember_user_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = MemberUserDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
