#encoding:utf-8
from app.system.services.setting_service import SettingService
from fastapi import APIRouter, Depends, Request, Response
from kxy.framework.friendly_exception import FriendlyException
from app.common.result import Result
from app.system.dal.sys_public_dictionary_type_dal import SysPublicDictionaryTypeDal
from app.common.filter import auth_module, get_current_user, tryCatch, get_admin_user
router = APIRouter()
from app.system.models.sys_public_dictionary_type import PublicDictionaryType
from app.system.services.excel_service import ExcelService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

@router.get("/sys_public_dictionary_type/list")
@auth_module(module_name="sys_public_dictionary_type", resource="list")
async def public_dictionary_type_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = SysPublicDictionaryTypeDal(request.state.db)
    data,total =await dal.Search(request.query_params,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/sys_public_dictionary_type/add")
@auth_module(module_name="sys_public_dictionary_type", resource="add")
async def public_dictionary_type_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysPublicDictionaryTypeDal(request.state.db)
    data = await dal.AddByJsonData(await request.json())
    return Result.success(data)

@router.post("/sys_public_dictionary_type/update")
@auth_module(module_name="sys_public_dictionary_type", resource="update")
async def public_dictionary_type_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysPublicDictionaryTypeDal(request.state.db)
    data = await dal.UpdateByJsonData(await request.json())
    return Result.success(data)

@router.get("/sys_public_dictionary_type/delete")
@auth_module(module_name="sys_public_dictionary_type", resource="delete")
async def public_dictionary_type_delete(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysPublicDictionaryTypeDal(request.state.db)
    await dal.Delete(id)
    logger.info(f"删除{id}成功")
    return Result.success("删除成功")
    
@router.post("/sys_public_dictionary_type/deletebatch")
@auth_module(module_name="sys_public_dictionary_type", resource="delete")
async def public_dictionary_type_deletebatch(request: Request,current_user: str = Depends(get_admin_user)):
    keys=request.json.get('keys')
    if keys:
        dal = SysPublicDictionaryTypeDal(request.state.db)
        dal.DeleteBatch(keys)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')

@router.get("/sys_public_dictionary_type/get")
@auth_module(module_name="sys_public_dictionary_type", resource="get")
async def public_dictionary_type_get(id,request: Request,current_user: str = Depends(get_admin_user)):
    dal = SysPublicDictionaryTypeDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)

@router.get("/sys_public_dictionary_type/export_excel")
@auth_module(module_name="sys_public_dictionary_type", resource="export_excel")
async def public_dictionary_type_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = SysPublicDictionaryTypeDal(request.state.db)
    await service.ExportExcel(PublicDictionaryType,SysPublicDictionaryTypeDal,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


# @router.get("/u/sys_public_dictionary_type/list")
# async def upublic_dictionary_type_list(request: Request,current_user: str = Depends(get_current_user)):
#     PageIndex = int(request.query_params.get("PageIndex", 1))
#     PageLimit = int(request.query_params.get("PageLimit", 10))
#     dal = PublicDictionaryTypeDal(request.state.db)
#     datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit)
#     return Result.pagesuccess(datas,total)

# @router.post("/u/sys_public_dictionary_type/add")
# async def upublic_dictionary_type_add(request: Request,current_user: str = Depends(get_current_user)):

#     dal = PublicDictionaryTypeDal(request.state.db)
#     data =await dal.AddByJsonDataUser(await request.json())
#     return Result.success(data)

# @router.post("/u/sys_public_dictionary_type/update")
# async def upublic_dictionary_type_update(request: Request,current_user: str = Depends(get_current_user)):
#     dal = PublicDictionaryTypeDal(request.state.db)
#     data =await dal.UpdateByJsonDataUser(await request.json())
#     return Result.success(data)

# @router.get("/u/sys_public_dictionary_type/delete/{id}")
# async def upublic_dictionary_type_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
#     dal = PublicDictionaryTypeDal(request.state.db)
#     data =await dal.DeleteByUser(id)
#     return Result.success("删除成功")
        
# @router.get("/u/sys_public_dictionary_type/get/{id}")
# async def upublic_dictionary_type_get(id:str,request: Request,current_user: str = Depends(get_current_user)):
#     dal = PublicDictionaryTypeDal(request.state.db)
#     data =await dal.GetExistByUser(id)
#     return Result.success(data)

@router.get("/sys_public_dictionary_type/user_editable_list")
@auth_module(module_name="sys_public_dictionary_type", resource="user_edit")
async def get_user_editable_public_dictionary_types(systemcode:str,request: Request, current_user: str = Depends(get_current_user)):
    """获取当前用户可编辑的public_dictionary字典类型"""
    service = SettingService(request.state.db)
    data = await service.get_user_editable_public_dictionary_types(systemcode)
    return Result.success(data)