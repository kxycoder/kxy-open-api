import re
from typing import Dict,List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.product.models.product_comment import ProductComment
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class ProductCommentDal(MyBaseDal[ProductComment]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(ProductComment,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[ProductComment]:
        return await self.QueryWhere([ProductComment.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[ProductComment],int]:
        fil = list()
        fil.append(ProductComment.deleted == 0)
        for k,v in search.items():
            if hasattr(ProductComment,k) and v:
                fil.append(getattr(ProductComment,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ProductComment.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ProductComment.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(ProductComment.DicType.ilike("%" + search_text + "%"),
            #                  ProductComment.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, ProductComment.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[ProductComment]:
        fil = list()
        fil.append( ProductComment.deleted == 0)
        for k,v in search.items():
            if hasattr(ProductComment,k) and v:
                fil.append(getattr(ProductComment,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( ProductComment.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( ProductComment. == int(status))
        items = await self.page_fields_nocount_query( ProductComment.get_mini_fields(), fil,  ProductComment.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->ProductComment:
        entity = ProductComment()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->ProductComment:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ProductComment=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([ProductComment.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([ProductComment.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[ProductComment],int]:
        fil = list()
        fil.append(ProductComment.userId == self.UserId)
        fil.append(ProductComment.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ProductComment.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ProductComment.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, ProductComment.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->ProductComment:
        entity = ProductComment()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.userId=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->ProductComment:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ProductComment=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.userId = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([ProductComment.id==id,ProductComment.userId==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([ProductComment.id.in_(ids),ProductComment.userId==self.UserId])

    async def ReplyComment(self, comment_id: int, reply_content: str) -> ProductComment:
        """
        回复评论
        :param comment_id: 评论ID
        :param reply_content: 回复内容
        :param admin_user: 管理员用户标识
        :return: 更新后的评论实体
        """
        # 获取评论实体
        entity: ProductComment = await self.GetExist(comment_id)

        # 更新回复相关字段
        entity.replyContent = reply_content
        entity.replyTime = datetime.now()
        entity.replyStatus = 1  # 1表示已回复

        # 保存更新
        await self.Update(entity)
        return entity

    async def UpdateVisible(self, comment_id: int, visible: bool) -> ProductComment:
        """
        更新评论可见性
        :param comment_id: 评论ID
        :param visible: 可见性状态 (true:显示 false:隐藏)
        :return: 更新后的评论实体
        """
        # 获取评论实体
        entity: ProductComment = await self.GetExist(comment_id)

        # 更新可见性字段
        entity.visible = visible

        # 保存更新（框架会自动处理 updater 和 updateTime）
        await self.Update(entity)
        return entity
