import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.pay.models.pay_app import PayApp
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class PayAppDal(MyBaseDal[PayApp]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(PayApp,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[PayApp]:
        return await self.QueryWhere([PayApp.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[PayApp],int]:
        fil = list()
        fil.append(PayApp.deleted == 0)
        for k,v in search.items():
            if hasattr(PayApp,k) and v:
                fil.append(getattr(PayApp,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayApp.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayApp.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(PayApp.DicType.ilike("%" + search_text + "%"),
            #                  PayApp.Description.ilike("%" + search_text + "%")))

        status = search.get('status')
        if status:
            fil.append(PayApp.status == int(status))

        items, total_count = await self.paginate_query(fil, PayApp.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[PayApp]:
        fil = list()
        fil.append( PayApp.deleted == 0)
        for k,v in search.items():
            if hasattr(PayApp,k) and v:
                fil.append(getattr(PayApp,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( PayApp.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( PayApp.status == int(status))
        items = await self.page_fields_nocount_query( PayApp.get_mini_fields(), fil,  PayApp.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->PayApp:
        entity = PayApp()
        entity.InitInsertEntityWithJson(jsonData)
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->PayApp:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayApp=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([PayApp.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([PayApp.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[PayApp],int]:
        fil = list()
        fil.append(PayApp.creator == self.UserId)
        fil.append(PayApp.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayApp.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayApp.Name.ilike("%" + search_text + "%"))

        status = search.get('status')
        if status:
            fil.append(PayApp.status == int(status))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, PayApp.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->PayApp:
        entity = PayApp()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.status = 0

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->PayApp:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayApp=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([PayApp.id==id,PayApp.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([PayApp.id.in_(ids),PayApp.creator==self.UserId])
