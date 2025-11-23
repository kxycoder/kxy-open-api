from contextvars import ContextVar
from datetime import timedelta
import datetime
import functools
import traceback
from uuid import uuid4
from fastapi import Request,status
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.contract.system.Imenu_busi import IMenuBusi
from app.global_var import Keys,Gkey
from app.config import config
from kxy.framework.friendly_exception import FriendlyException, NoLoginException
from app.common.result import Result
from app.database import AsyncSessionLocal
from app.contract.system.Iuser_service import IUserService
from app.tools import utils
from kxy.framework.context import trace_id,session_id,user_id,user_info,current_tenant_id,kxy_roles,access_token
from app.database import redisClient
from jose import jwt
from kxy.framework.mapper import Mapper

from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

family_id = ContextVar("family_id", default='0')

def getRoles():
    return kxy_roles.get()
async def check_schema(schema):
    userid = user_id.get()
    if userid=='0':
        return False
    tenantId = current_tenant_id.get()
    # 构造 Redis 中的权限键
    redis_key = Gkey(Keys.USER_SCHEMAS,tenantId,userid,schema)
    
    # 尝试从 Redis 中获取权限
    permission = await redisClient.get_string(redis_key)
    if permission is not None:
        # 如果 Redis 中存在权限信息，直接返回
        return permission == "1"
    if 'super_admin' in getRoles():
        return True
    async with AsyncSessionLocal() as session:
        busi = Mapper.getservice_by_contract(IUserService,session)
        has_permission = await busi.CheckSchema(userid,schema)
        if config.ignor_auth == 1:
            has_permission = True
        has_permission_cache = '1' if has_permission else '0'
        result = await redisClient.set(redis_key, has_permission_cache, ex=timedelta(days=1))
        print(result)
        return has_permission
async def check_module(moduleName,resource):
    userid = user_id.get()
    if userid=='0':
        return False
    # 构造 Redis 中的权限键
    redis_key = Gkey(Keys.USER_PERMISSION,config.SystemCode,userid,moduleName,resource)
    
    # 尝试从 Redis 中获取权限
    permission = await redisClient.get_string(redis_key)
    if permission is not None:
        # 如果 Redis 中存在权限信息，直接返回
        return permission == "1"
    if 'super_admin' in getRoles():
        return True
    async with AsyncSessionLocal() as session:
        busi = Mapper.getservice_by_contract(IMenuBusi,session)
        # systemCode,userId,permissions
        has_permission = await busi.CheckPermission(config.SystemCode,userid,f'{moduleName}${resource}')
        if config.ignor_auth == 1:
            has_permission = True
        has_permission_cache = '1' if has_permission else '0'
        result = await redisClient.set(redis_key, has_permission_cache, ex=timedelta(days=1))
        print(result)
        return has_permission
    
    # 如果 Redis 中不存在，则从 sso.ezrpro.com 获取权限
    # async with httpx.AsyncClient() as client:
    #     url = f"{config.AUTH_URL}checkPermission?systemCode=publish_tool&permissions={moduleName}${resource}&userId={user_id}"
    #     response =await client.get(url)
    #     if response.status_code == 200:
    #         data = response.text
    #         has_permission = '0'
    #         if data=='true':
    #             has_permission='1'
    #         # 将权限信息存储在 Redis 中，设置一天的失效时间
    #         await redis_client.set(redis_key, has_permission, ex=timedelta(days=1))
    #         return has_permission=='1'
    #     else:
    #         # 如果请求失败，记录错误并返回 False
    #         logger.error(f"Failed to fetch permission from sso.ezrpro.com: {response.status}")
    #         return False
def get_access_token_from_authorization_header(request: Request):
    """
    从Authorization头中提取Bearer Token
    """
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header[7:]  # 去掉'Bearer '前缀
    return None
async def tracing_middleware(request: Request, call_next):
    # 生成唯一trace_id
    req_trace_id = request.headers.get("x-trace-id") or str(uuid4())
    trace_id.set(req_trace_id)
    session_id.set(str(uuid4()))
    msg = f"{request.method} {request.url}"
    logger.info(msg)
    # jwt实现，注释掉了，如果需要使用jwt模式，自行打开
    # token_key = 'X-Token'
    # token = request.headers.get(token_key) or request.cookies.get(token_key) or request.query_params.get(token_key)
    # if token and token not in ['undefined','None']:
    #     access_token.set(token)
    #     try:
    #         userInfo = jwt.decode(token=token,key=config.JWT_SECRET_KEY,algorithms=config.JWT_ALGORITHM)
    #         if userInfo.get('exp',0)<=int(datetime.datetime.now().timestamp()):
    #             raise NoLoginException()
    #         user_info.set(userInfo)
    #         user_id.set(userInfo.get('id'))
    #         kxy_roles.set(userInfo.get('roles'))
    #     except Exception as e:
    #         logger.error(f"jwt_token解析失败:{token},ex:{e}")
    token = get_access_token_from_authorization_header(request)
    if token:
        access_token.set(token)
        cacheKey = Gkey(Keys.USER_API_TOKEN,token)
        userInfo = await redisClient.get_json(cacheKey)
        if userInfo:
            user_info.set(userInfo)
            userid = userInfo.get('id')
            user_id.set(userid)
            current_tenant_id.set(userInfo.get('tenantId'))
            async with AsyncSessionLocal() as session:
                busi = Mapper.getservice_by_contract(IUserService,session)
                roles = await busi.GetUserRolesNameCache(userid,False)
                kxy_roles.set(roles)
    try:
        response = await call_next(request)
        response.headers["x-trace-id"] = req_trace_id
        if response.status_code == 401:
            return JSONResponse(content=Result.error401(), status_code=200)
        return response
    except FriendlyException as fex:
        res = Result.friendlyerror(str(fex))
        # return res
        return JSONResponse(content=res, status_code=200)
    except HTTPException as he:
        res = Result.error(str(he),errcode=he.status_code)
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        logger.error(f'执行{msg}，出错:{e},堆栈:{traceback.format_exc(limit=20)}')
        if config.ENV_NAME!='production':
            return JSONResponse(content=Result.error(str(e)), status_code=200)
        else:
            return JSONResponse(content=Result.error("程序发生错误，正在抢修"), status_code=200)
async def db_session_middleware(request: Request, call_next):
    async with AsyncSessionLocal() as session:
        request.state.db = session
        # session.refresh() 
        response = await call_next(request)
    return response
async def get_current_user():
    '''获取登录用户'''
    userid = user_id.get()
    if userid=='0':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return userid
async def get_admin_user():
    '''获取后台登录用户'''
    userid = user_id.get()
    if userid=='0':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="请先登录",
            headers={"WWW-Authenticate": "Bearer"},
        )
    roles = kxy_roles.get()
    if not roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是后台用户",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return userid

def auth_module(module_name, resource):
    def decorator(f):
        @functools.wraps(f)
        async def decorated_function(*args, **kwargs):
            has_permission=await check_module(module_name,resource)
            if not has_permission:
                logger.error(f"用户没有权限访问{module_name}模块的{resource}资源")
                return Result.friendlyerror(f"用户没有权限访问{module_name}模块的{resource}资源")
            return await f(*args, **kwargs)
        return decorated_function
    return decorator
def auth_schema(schema):
    def decorator(f):
        @functools.wraps(f)
        async def decorated_function(*args, **kwargs):
            has_permission=await check_schema(schema)
            if not has_permission:
                logger.error(f"用户没有模块{schema}的权限")
                return Result.friendlyerror(f"用户没有模块{schema}的权限")
            return await f(*args, **kwargs)
        return decorated_function
    return decorator

def tryCatch(f):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except FriendlyException as fex:
            return Result.friendlyerror(str(fex))
        except Exception as e:
            logger.error(f'执行{f.__name__}，参数:{args},{kwargs}，出错:{e}')
            return Result.error("程序发生错误，正在抢修")
    return wrapper