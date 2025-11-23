from datetime import datetime
from PIL import Image
import os
import shutil
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Request,status
from fastapi.responses import FileResponse, JSONResponse
from app.config import config
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.sys_users_dal import SysUsersDal
from app.common.filter import auth_module, get_current_user, tryCatch, get_admin_user
router = APIRouter()
from app.system.services.menu_busi import MenuBusi
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)
from kxy.framework.util import SUtil
from app.system.services.user_service import UserService

@router.get("/sys_users/list")
@auth_module(module_name="sys_users", resource="list")
async def sys_users_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = SysUsersDal(request.state.db)
    data,total =await dal.Search(request.query_params,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)
@router.get("/user/simple-list")
@auth_module(module_name="sys_users", resource="list")
async def sys_users_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    # dal = SystemDeptDal(request.state.db)
    search = {**request.query_params}
    dal = SysUsersDal(request.state.db)
    data =await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(data)

@router.post("/sys_users/add")
@auth_module(module_name="sys_users", resource="add")
async def sys_users_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysUsersDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data.to_basic_dict())

@router.post("/sys_users/update")
@auth_module(module_name="sys_users", resource="update")
async def sys_users_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysUsersDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data.to_basic_dict())

@router.get("/sys_users/delete/{id}")
@auth_module(module_name="sys_users", resource="delete")
async def sys_users_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysUsersDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.post("/sys_users/deletebatch")
@auth_module(module_name="sys_users", resource="delete")
async def sys_users_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    jsonData = await request.json()
    keys=jsonData.get('keys')
    if keys:
        dal = SysUsersDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/sys_users/get/{id}")
@auth_module(module_name="sys_users", resource="get")
async def sys_users_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysUsersDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data.to_basic_dict())

@router.get("/user/login_wx")
async def opt_sso_users_login_wx(request: Request):
    rdata = request.query_params
    code = SUtil.get_arg(rdata, 'code', '微信授权码')
    sourceId = rdata.get('sourceId')
    sourceType = rdata.get('sourceType')
    sourceUser =  rdata.get('sourceUser')
    userSvc = UserService(request.state.db)
    data =await userSvc.LoginWx(code,sourceUser,sourceId,sourceType)
    if data is None:
        return Result.friendlyerror("用户名或者密码错误")
    jwt_token = data.get('token')
    success = Result.success(data)
    response = JSONResponse(content=success)
    response.set_cookie(key="X-Token", value=jwt_token, httponly=True)
    return response

# login


    
@router.get("/user/user_info")
async def opt_sso_users_info(request: Request,current_user: str = Depends(get_current_user)):
    token=request.query_params.get('token')
    if token =='':
        raise FriendlyException('请输入token')
    
    dal = SysUsersDal(request.state.db)
    data =await dal.Get(current_user)
    if data is None:
        return Result.friendlyerror("token不存在或者已经过期")
    data.Roles = await MenuBusi(request.state.db).GetUserRolesNameCache(config.SystemCode,current_user)
    return Result.success(data)
@router.get('/user/wx_phone')
async def opt_sso_users_wx_phone(request: Request,code:str):
    userSvc = UserService(request.state.db)
    data =await userSvc.UpdateUserPhone(code)
    return {'ok'}
@router.get("/user/info")
async def opt_sso_users_info(request: Request,current_user: str = Depends(get_current_user)):
    try:
        userSvc = UserService(request.state.db)
        data =await userSvc.GetUserInfo()
        return Result.success(data.to_mini_dict())
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
@router.post("/file/upload")
async def opt_sso_users_upload(request: Request, current_user: str = Depends(get_current_user)):
    form = await request.form()
    file = form.get('file')
    headImage = form.get('headImage')
    if not file:
        raise FriendlyException('未找到要上传的文件')
    now = datetime.now()
    fileName = f'{now.year}/{now.month}/{now.day}/{uuid4()}.{file.content_type.split("/")[-1]}'
    root_path = os.path.join(os.getcwd(), config.UPLOAD_FILEPATH)
    file_path = os.path.join(root_path,f'{now.year}/{now.month}/{now.day}')
    originPath = os.path.join(root_path,f'origin/{now.year}/{now.month}/{now.day}')
    if os.path.exists(file_path) == False:
        os.makedirs(file_path)
    if os.path.exists(originPath) == False:
        os.makedirs(originPath)
        
    file_path = os.path.join(root_path, fileName)
    orgin_file_path = os.path.join(root_path,f'origin/{fileName}')
    url=f"/{fileName}"
    originFileName = f'/origin{url}'
    if headImage:
        
        with Image.open(file.file) as img:
            # 计算等比例缩放后的尺寸
            maxSize = max(img.size)
            if maxSize > 400:
                ratio = 400/max(img.size)
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.LANCZOS)
            img.save(orgin_file_path)
            if maxSize>200:
                ratio = 200/max(img.size)
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.LANCZOS)
            img.save(file_path, quality=100, optimize=False)
    else:
        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return Result.success({"url":url,'origin':originFileName})
@router.post("/user/update_userInfo_wx")
async def update_userInfo(request: Request,current_user: str = Depends(get_current_user)):
    jsonData = await request.json()
    # {"Sex":"1","NickName":"路人甲","Avater":"http://tmp/fzC3lYdBbHHP3c9404e269880df7d7370d26e9f89fdf.jpeg","summary":"我是一个好人"}
    userSvc = UserService(request.state.db)
    await userSvc.UpdateUserInfo(jsonData)
    return Result.success({"message":"ok"})
@router.get("/user/update_nickname")
async def update_userInfo(NickName:str,request: Request,current_user: str = Depends(get_current_user)):
    # {"Sex":"1","NickName":"路人甲","Avater":"http://tmp/fzC3lYdBbHHP3c9404e269880df7d7370d26e9f89fdf.jpeg","summary":"我是一个好人"}
    if NickName == '':
        return Result.error("昵称不能为空")
    PhoneNumber = request.query_params.get('PhoneNumber')
    userSvc = UserService(request.state.db)
    await userSvc.UpdateNickName(NickName,PhoneNumber)
    return Result.success({"message":"ok"})

@router.get('/user/file/{filePath:path}')
async def get_file(request: Request,filePath:str):
    root_path = os.path.join(os.getcwd(), config.UPLOAD_FILEPATH)
    file_path = os.path.join(root_path,filePath)
    if os.path.exists(file_path) == False:
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(file_path)