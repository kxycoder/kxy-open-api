from fastapi import APIRouter, Depends, Request
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.result import Result
from app.product.dal.product_comment_dal import ProductCommentDal
from app.common.filter import auth_schema, get_current_user, get_admin_user
from app.product.models.product_comment import ProductComment
from app.product.services.product_service import ProductService
from app.system.services.excel_service import ExcelService
from logging import getLogger

logger = getLogger(__name__)
router = APIRouter()

@router.get("/comment/simple-list")
@auth_schema("product:comment:query")
async def product_comment_simple_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = ProductCommentDal(request.state.db)
    search = {**request.query_params}
    datas = await dal.GetSimpleList(search,PageIndex, PageLimit)
    return Result.success(datas)


@router.get("/comment/page")
@auth_schema("product:comment:query")
async def product_comment_list(request: Request,current_user: str = Depends(get_admin_user)):
    PageIndex = int(request.query_params.get("pageNo", 1))
    PageLimit = int(request.query_params.get("pageSize", 10))
    dal = ProductService(request.state.db)
    search = {**request.query_params}
    data,total =await dal.GetCommentList(search,PageIndex, PageLimit)
    return Result.pagesuccess(data,total)

@router.post("/comment/create")
@auth_schema("product:comment:create")
async def product_comment_add(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductCommentDal(request.state.db)
    jsonData = await request.json()
    data = await dal.AddByJsonData(jsonData)

    return Result.success(data)

@router.put("/comment/update")
@auth_schema("product:comment:update")
async def product_comment_update(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductCommentDal(request.state.db)
    jsonData = await request.json()
    data = await dal.UpdateByJsonData(jsonData)

    return Result.success(data)


@router.post("/comment/save")
@auth_schema("product:comment:update")
async def product_comment_save(request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductCommentDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonData(jsonData)
    else:
        data =await dal.AddByJsonData(jsonData)
    return Result.success(data)


@router.delete("/comment/delete")
@auth_schema("product:comment:delete")
async def product_comment_delete(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductCommentDal(request.state.db)
    await dal.Delete(id)
    return Result.success("删除成功")


    
@router.delete("/comment/delete-list")
@auth_schema("product:comment:delete")
async def product_comment_deletebatch(ids:str,request: Request,current_user: str = Depends(get_admin_user)):
    ids = [int(i) for i in ids.split(",")]
    if ids:
        dal = ProductCommentDal(request.state.db)
        await dal.DeleteBatch(ids)
        return Result.success("删除成功")
    else:
        raise FriendlyException('请传入要删除的行')


@router.get("/comment/get")
@auth_schema("product:comment:query")
async def product_comment_get(id:int,request: Request,current_user: str = Depends(get_admin_user)):
    dal = ProductCommentDal(request.state.db)
    data =await dal.Get(id)
    return Result.success(data)


@router.get("/comment/export-excel")
@auth_schema("product:comment:export")
async def product_comment_export_excel(request: Request,current_user: str = Depends(get_admin_user)):
    service = ExcelService(request.state.db)
    dal = ProductCommentDal(request.state.db)
    await service.ExportExcel(ProductComment,dal.Search,request.query_params)
    return Result.success("成功加入导出队列，请稍后下载")


@router.get("/u/comment/list")
async def uproduct_comment_list(request: Request,current_user: str = Depends(get_current_user)):
    PageIndex = int(request.query_params.get("PageIndex", 1))
    PageLimit = int(request.query_params.get("PageLimit", 10))
    dal = ProductCommentDal(request.state.db)
    datas,total =await dal.SearchByUser(request.query_params,PageIndex, PageLimit,False)
    return Result.pagesuccess(datas,total)

@router.post("/u/comment/add")
async def uproduct_comment_add(request: Request,current_user: str = Depends(get_current_user)):


    dal = ProductCommentDal(request.state.db)
    data =await dal.AddByJsonDataUser(await request.json())
    return Result.success(data)


@router.put("/u/comment/update")
async def uproduct_comment_update(request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductCommentDal(request.state.db)
    data =await dal.UpdateByJsonDataUser(await request.json())
    return Result.success(data)


@router.post("/u/comment/save")
async def uproduct_comment_save(request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductCommentDal(request.state.db)
    jsonData = await request.json()
    if jsonData.get('id'):
        data =await dal.UpdateByJsonDataUser(jsonData)
    else:
        data =await dal.AddByJsonDataUser(jsonData)
    return Result.success(data)


@router.delete("/u/comment/delete")
async def uproduct_comment_delete(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductCommentDal(request.state.db)
    data =await dal.DeleteByUser(id)
    return Result.success("删除成功")
        
@router.get("/u/comment/get")
async def uproduct_comment_get(id:int,request: Request,current_user: str = Depends(get_current_user)):
    dal = ProductCommentDal(request.state.db)
    data =await dal.GetExistByUser(id)
    return Result.success(data)

# /comment/reply
@router.put("/comment/reply")
@auth_schema("product:comment:update")
async def product_comment_reply(request: Request, current_user: str = Depends(get_admin_user)):
    """
    评论回复接口
    接收参数: {"id": 评论ID, "replyContent": "回复内容"}
    """
    dal = ProductCommentDal(request.state.db)
    jsonData = await request.json()

    # 获取评论ID和回复内容
    comment_id = jsonData.get('id')
    reply_content = jsonData.get('replyContent')

    if not comment_id:
        raise FriendlyException('评论ID不能为空')
    if not reply_content:
        raise FriendlyException('回复内容不能为空')

    # 回复评论
    data = await dal.ReplyComment(comment_id, reply_content)
    return Result.success(data)

# /comment/update-visible
@router.put("/comment/update-visible")
@auth_schema("product:comment:update")
async def product_comment_update_visible(request: Request, current_user: str = Depends(get_admin_user)):
    """
    更新评论可见性接口
    接收参数: {"id":11,"visible":false}
    """
    dal = ProductCommentDal(request.state.db)
    jsonData = await request.json()

    # 获取评论ID和可见性
    comment_id = jsonData.get('id')
    visible = jsonData.get('visible')

    if comment_id is None:
        raise FriendlyException('评论ID不能为空')
    if visible is None:
        raise FriendlyException('可见性状态不能为空')

    data = await dal.UpdateVisible(comment_id, visible)
    return Result.success(data)