from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.member.dal.member_sign_in_config_dal import MemberSignInConfigDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.member.models.member_sign_in_config import MemberSignInConfig
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/sign-in-config/simple-list")
@auth_schema("member:sign-in-config:query")
async def member_sign_in_config_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = MemberSignInConfigDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/sign-in-config/page")
@auth_schema("member:sign-in-config:query")
async def member_sign_in_config_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = MemberSignInConfigDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/sign-in-config/create")
@auth_schema("member:sign-in-config:create")
async def member_sign_in_config_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberSignInConfigDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/sign-in-config/update")
@auth_schema("member:sign-in-config:update")
async def member_sign_in_config_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberSignInConfigDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/sign-in-config/save")
@auth_schema("member:sign-in-config:update")
async def member_sign_in_config_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberSignInConfigDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/sign-in-config/delete")
@auth_schema("member:sign-in-config:delete")
async def member_sign_in_config_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberSignInConfigDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/sign-in-config/delete-list")
@auth_schema("member:sign-in-config:delete")
async def member_sign_in_config_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = MemberSignInConfigDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/sign-in-config/get")
@auth_schema("member:sign-in-config:query")
async def member_sign_in_config_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = MemberSignInConfigDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/sign-in-config/export-excel")
@auth_schema("member:sign-in-config:export")
async def member_sign_in_config_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = MemberSignInConfigDal(request.state.db)
    await service.ExportExcel(MemberSignInConfig,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/sign-in-config/list")
async def umember_sign_in_config_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = MemberSignInConfigDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/sign-in-config/add")
async def umember_sign_in_config_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = MemberSignInConfigDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/sign-in-config/update")
async def umember_sign_in_config_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = MemberSignInConfigDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/sign-in-config/save")
async def umember_sign_in_config_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = MemberSignInConfigDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('Id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/sign-in-config/delete")
async def umember_sign_in_config_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = MemberSignInConfigDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/sign-in-config/get")
async def umember_sign_in_config_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = MemberSignInConfigDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)
