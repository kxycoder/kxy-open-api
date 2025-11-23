import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.kxy.models.kxy_demo03_student import KxyDemo03Student
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class KxyDemo03StudentDal(MyBaseDal[KxyDemo03Student]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(KxyDemo03Student,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[KxyDemo03Student]:
        return await self.QueryWhere([KxyDemo03Student.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[KxyDemo03Student],int]:
        fil = list()
        fil.append(KxyDemo03Student.deleted == 0)
        for k,v in search.items():
            if hasattr(KxyDemo03Student,k) and v:
                fil.append(getattr(KxyDemo03Student,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(KxyDemo03Student.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(KxyDemo03Student.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(KxyDemo03Student.DicType.ilike("%" + search_text + "%"),
            #                  KxyDemo03Student.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_fields_query(KxyDemo03Student.get_mini_fields(), fil, KxyDemo03Student.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[KxyDemo03Student]:
        fil = list()
        fil.append( KxyDemo03Student.deleted == 0)
        for k,v in search.items():
            if hasattr(KxyDemo03Student,k) and v:
                fil.append(getattr(KxyDemo03Student,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( KxyDemo03Student.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( KxyDemo03Student. == int(status))
        items = await self.page_fields_nocount_query( KxyDemo03Student.get_mini_fields(), fil,  KxyDemo03Student.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->KxyDemo03Student:
        entity = KxyDemo03Student()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->KxyDemo03Student:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:KxyDemo03Student=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([KxyDemo03Student.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([KxyDemo03Student.id.in_(ids)])
 
