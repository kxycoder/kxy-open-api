from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.api.types.vo_request import VoSocialAuthRedirect
from app.system.dal.system_social_user_dal import SystemSocialUserDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.system.models.system_social_user import SystemSocialUser
from app.system.services.excel_service import ExcelService
router = APIRouter()
from app.system.services.user_service import UserService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/social-user/simple-list")
@auth_schema("system:social-user:query")
async def system_social_user_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemSocialUserDal(request.state.db)
    search = {**request.query_params}

    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)

@router.get("/social-user/page")
@auth_schema("system:social-user:query")
async def system_social_user_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = SystemSocialUserDal(request.state.db)
    search = {**request.query_params}
    data,total =await dal.Search(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/social-user/create")
@auth_schema("system:social-user:create")
async def system_social_user_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSocialUserDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.put("/social-user/update")
@auth_schema("system:social-user:update")
async def system_social_user_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSocialUserDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.post("/social-user/save")
@auth_schema("system:social-user:update")
async def system_social_user_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSocialUserDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)

@router.delete("/social-user/delete")
@auth_schema("system:social-user:delete")
async def system_social_user_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSocialUserDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.delete("/social-user/delete-list")
@auth_schema("system:social-user:delete")
async def system_social_user_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = SystemSocialUserDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/social-user/get")
@auth_schema("system:social-user:query")
async def system_social_user_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SystemSocialUserDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/social-user/export-excel")
@auth_schema("system:social-user:export")
async def system_social_user_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SystemSocialUserDal(request.state.db)
    await service.ExportExcel(SystemSocialUser,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")

# /social-user/get-bind-list
@router.get("/social-user/get-bind-list")
@auth_schema("system:social-user:query")
async def system_social_user_get_bind_list(request: Request,current_user: str = Depends(get_admin_user)):
    dal = UserService(request.state.db)
    data =await dal.GetSocialUserBinding()
    return Result.success(data)


# /auth/social-auth-redirect?type=20&redirectUri=http%3A%2F%2Fyudao.forwework.com%2Fuser%2Fprofile%3Ftype%253D20
@router.get('/auth/social-auth-redirect')
async def opt_sso_users_social_auth_redirect(type:int,redirectUri:str,request: Request):
    socialSvc = UserService(request.state.db)
    data =await socialSvc.SocialAuthRedirect(type,redirectUri)
    return Result.success(data)
# /system/social-user/bind
@router.post('/social-user/bind')
async def opt_sso_users_bind(request: Request,current_user: str = Depends(get_current_user)):
    requestData = await request.json()
    socialSvc = UserService(request.state.db)
    data =await socialSvc.BindingSocialUser(requestData)
    return Result.success(True)

# /social-user/unbind
@router.delete('/social-user/unbind')
async def opt_sso_users_unbind(request: Request,current_user: str = Depends(get_current_user)):
    requestData = await request.json()
    socialSvc = UserService(request.state.db)
    data =await socialSvc.UnbindingSocialUser(requestData)
    return Result.success(True)

# /auth/social-login
@router.post('/auth/social-login')
async def opt_sso_users_social_login(request: Request,data:VoSocialAuthRedirect):
    # {"type":"20","code":"06562527cabf33b9a88d4dd601a46bea","state":"4789fe9dd387443e996d9c14e5398289"}
    requestData = await request.json()
    socialSvc = UserService(request.state.db)
    data =await socialSvc.SocialLogin(data)
    return Result.success(data)