import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.kxy.models.kxy_demo01_contact import KxyDemo01Contact
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class KxyDemo01ContactDal(MyBaseDal[KxyDemo01Contact]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(KxyDemo01Contact,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[KxyDemo01Contact]:
        return await self.QueryWhere([KxyDemo01Contact.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[KxyDemo01Contact],int]:
        fil = list()
        fil.append(KxyDemo01Contact.deleted == 0)
        for k,v in search.items():
            if hasattr(KxyDemo01Contact,k) and v:
                fil.append(getattr(KxyDemo01Contact,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(KxyDemo01Contact.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(KxyDemo01Contact.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(KxyDemo01Contact.DicType.ilike("%" + search_text + "%"),
            #                  KxyDemo01Contact.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_fields_query(KxyDemo01Contact.get_mini_fields(), fil, KxyDemo01Contact.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[KxyDemo01Contact]:
        fil = list()
        fil.append( KxyDemo01Contact.deleted == 0)
        for k,v in search.items():
            if hasattr(KxyDemo01Contact,k) and v:
                fil.append(getattr(KxyDemo01Contact,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( KxyDemo01Contact.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( KxyDemo01Contact. == int(status))
        items = await self.page_fields_nocount_query( KxyDemo01Contact.get_mini_fields(), fil,  KxyDemo01Contact.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->KxyDemo01Contact:
        entity = KxyDemo01Contact()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->KxyDemo01Contact:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:KxyDemo01Contact=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([KxyDemo01Contact.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([KxyDemo01Contact.id.in_(ids)])
 
