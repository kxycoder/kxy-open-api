import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.kxy.models.kxy_demo02_category import KxyDemo02Category
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class KxyDemo02CategoryDal(MyBaseDal[KxyDemo02Category]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(KxyDemo02Category,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[KxyDemo02Category]:
        return await self.QueryWhere([KxyDemo02Category.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[KxyDemo02Category],int]:
        fil = list()
        fil.append(KxyDemo02Category.deleted == 0)
        for k,v in search.items():
            if hasattr(KxyDemo02Category,k) and v:
                fil.append(getattr(KxyDemo02Category,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(KxyDemo02Category.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(KxyDemo02Category.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(KxyDemo02Category.DicType.ilike("%" + search_text + "%"),
            #                  KxyDemo02Category.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_fields_query(KxyDemo02Category.get_mini_fields(), fil, KxyDemo02Category.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[KxyDemo02Category]:
        fil = list()
        fil.append( KxyDemo02Category.deleted == 0)
        for k,v in search.items():
            if hasattr(KxyDemo02Category,k) and v:
                fil.append(getattr(KxyDemo02Category,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( KxyDemo02Category.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( KxyDemo02Category. == int(status))
        items = await self.page_fields_nocount_query( KxyDemo02Category.get_mini_fields(), fil,  KxyDemo02Category.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->KxyDemo02Category:
        entity = KxyDemo02Category()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->KxyDemo02Category:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:KxyDemo02Category=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def GetListByParentIds(self,parentIds:List[int])->List[KxyDemo02Category]:
        return await self.QueryWhere([KxyDemo02Category.parentId.in_(parentIds),KxyDemo02Category.deleted==0])

    async def DeleteByParentId(self,parentIds):
        childrens = await self.GetListByParentIds(parentIds)
        if not childrens:
            return
        ids = [x.id for x in childrens]
        await self.DeleteBatch(ids)
        await self.DeleteByParentId(ids)

    async def Delete(self,id):
        await self.DeleteWhere([KxyDemo02Category.id==id])
        await self.DeleteByParentId([id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([KxyDemo02Category.id.in_(ids)])
 
