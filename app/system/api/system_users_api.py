from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from kxy.framework.friendly_exception import FriendlyException
from app.contract.types.user_vo import VoUserInfo, VoUserProfilePass
from app.common.result import Result
from app.system.api.types.vo_request import VoRegistTenant
from app.system.dal.system_users_dal import SystemUsersDal
from app.common.filter import auth_module, get_current_user, get_admin_user, auth_schema
from app.system.models.system_users import SystemUsers
from app.system.services.excel_service import ExcelService
router = APIRouter()
from app.system.services.orgnization_service import OrgnizationService
from app.system.services.tenant_service import TenantService
from app.system.services.user_service import UserService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/user/simple-list")
@auth_schema("system:user:query")
async def system_users_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemUsersDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/user/page")
@auth_schema("system:user:query")
async def system_users_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemUsersDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/user/create")
@auth_schema("system:user:create")
async def system_users_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUsersDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data.to_mini_dict())

@router.put("/user/update")
@auth_schema("system:user:update")
async def system_users_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUsersDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.put('/user/profile/update')
async def system_users_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUsersDal(request.state.db)
    data = await dal.UpdateMyprofile(await request.json())
    return Result.success(data)

@router.post("/user/save")
@auth_schema("system:user:update")
async def system_users_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUsersDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/user/delete")
@auth_schema("system:user:delete")
async def system_users_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    svc = UserService(request.state.db)
    await svc.DeleteUser(id)
    return Result.success(True)
    
@router.delete("/user/delete-list")
@auth_schema("system:user:delete")
async def system_users_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SystemUsersDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/user/get")
@auth_schema("system:user:query")
async def system_users_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemUsersDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data.to_mini_dict())

@router.get("/user/export-excel")
@auth_schema("system:user:export")
async def system_users_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemUsersDal(request.state.db)
    await service.ExportExcel(SystemUsers,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


# /user/update-password
@router.put("/user/update-password")
@auth_schema("system:user:update-password")
async def system_users_update_password(userInfo:VoUserInfo,request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemUsersDal(request.state.db)
    data =await dal.UpdatePassword(userInfo)
    return Result.success(True)

@router.put("/user/profile/update-password")
async def system_users_update_password(userInfo:VoUserProfilePass,request: Request,current_user: str = Depends(get_current_user)):
    dal = SystemUsersDal(request.state.db)
    data =await dal.UpdateMyPassword(userInfo)
    return Result.success(True)

@router.post("/user/login")
async def opt_sso_users_login(request: Request,):
    rdata= await request.json()
    username=rdata.get('username','')
    password=rdata.get('password','')
    if username =='':
        raise FriendlyException('请输入用户名')
    if password =='':
        raise FriendlyException('请传入密码')
    logger.info("user:%s,login now"%username)

    userSvc = UserService(request.state.db)
    data =await userSvc.Login(username,password)
    
    if data is None:
        return Result.friendlyerror("用户名或者密码错误")
    jwt_token = data.get('token')
    success = Result.success(data)
    response = JSONResponse(content=success)
    response.set_cookie(key="X-Token", value=jwt_token, httponly=True)
    return response

# /system/auth/register
@router.post('/auth/register')
async def opt_sso_users_register(request: Request,registData:VoRegistTenant):
    userSvc = TenantService(request.state.db)
    data = await userSvc.RegisteTenant(registData)
    return Result.success(data)

# /user/update-status
@router.put("/user/update-status")
@auth_schema("system:user:update-status")
async def system_users_update_status(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    id=jsonData.get('id')
    status=jsonData.get('status')
    if id is None:
        raise FriendlyException('请传入用户ID')
    if status is None:
        raise FriendlyException('请传入用户状态')
    userSvc = UserService(request.state.db)
    await userSvc.UpdateUserStatus(id,status)
    return Result.success(True)
@router.post('/auth/logout')
async def opt_sso_users_logout(request: Request, current_user: str = Depends(get_current_user)):
    userSvc = UserService(request.state.db)
    data =await userSvc.Logout()
    return Result.success(True)

@router.post('/auth/refresh-token')
async def opt_sso_users_refresh_token(refreshToken:str,request: Request):
    if not refreshToken:
        raise FriendlyException('请传入refreshToken')
    userSvc = UserService(request.state.db)
    data =await userSvc.RefreshToken(refreshToken)
    return Result.success(data)

# /profile/get
@router.get('/user/profile/get')
@auth_schema("system:user:query")
async def system_users_profile_get(request: Request,current_user: str = Depends(get_current_user)):
    userSvc = UserService(request.state.db)
    data =await userSvc.GetProfile()
    return Result.success(data)

@router.put('/user/sync-user')
@auth_schema("system:user:sync")
async def system_users_sync_user(request: Request,current_user: str = Depends(get_admin_user)):
    svc = OrgnizationService(request.state.db)
    await svc.sync_users_to_system_users()
    return Result.success("同步成功")