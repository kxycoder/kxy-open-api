import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.pay.models.pay_order_extension import PayOrderExtension
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class PayOrderExtensionDal(MyBaseDal[PayOrderExtension]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(PayOrderExtension,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[PayOrderExtension]:
        return await self.QueryWhere([PayOrderExtension.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[PayOrderExtension],int]:
        fil = list()
        fil.append(PayOrderExtension.deleted == 0)
        for k,v in search.items():
            if hasattr(PayOrderExtension,k) and v:
                fil.append(getattr(PayOrderExtension,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayOrderExtension.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayOrderExtension.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(PayOrderExtension.DicType.ilike("%" + search_text + "%"),
            #                  PayOrderExtension.Description.ilike("%" + search_text + "%")))

        status = search.get('status')
        if status:
            fil.append(PayOrderExtension.status == int(status))

        items, total_count = await self.paginate_query(fil, PayOrderExtension.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[PayOrderExtension]:
        fil = list()
        fil.append( PayOrderExtension.deleted == 0)
        for k,v in search.items():
            if hasattr(PayOrderExtension,k) and v:
                fil.append(getattr(PayOrderExtension,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( PayOrderExtension.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( PayOrderExtension.status == int(status))
        items = await self.page_fields_nocount_query( PayOrderExtension.get_mini_fields(), fil,  PayOrderExtension.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->PayOrderExtension:
        entity = PayOrderExtension()
        entity.InitInsertEntityWithJson(jsonData)
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->PayOrderExtension:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayOrderExtension=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([PayOrderExtension.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([PayOrderExtension.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[PayOrderExtension],int]:
        fil = list()
        fil.append(PayOrderExtension.creator == self.UserId)
        fil.append(PayOrderExtension.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayOrderExtension.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayOrderExtension.Name.ilike("%" + search_text + "%"))

        status = search.get('status')
        if status:
            fil.append(PayOrderExtension.status == int(status))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, PayOrderExtension.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->PayOrderExtension:
        entity = PayOrderExtension()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.status = 0

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->PayOrderExtension:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayOrderExtension=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([PayOrderExtension.id==id,PayOrderExtension.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([PayOrderExtension.id.in_(ids),PayOrderExtension.creator==self.UserId])
