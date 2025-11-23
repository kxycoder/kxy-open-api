import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.pay.models.pay_refund import PayRefund
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class PayRefundDal(MyBaseDal[PayRefund]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(PayRefund,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[PayRefund]:
        return await self.QueryWhere([PayRefund.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[PayRefund],int]:
        fil = list()
        fil.append(PayRefund.deleted == 0)
        for k,v in search.items():
            if hasattr(PayRefund,k) and v:
                fil.append(getattr(PayRefund,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayRefund.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayRefund.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(PayRefund.DicType.ilike("%" + search_text + "%"),
            #                  PayRefund.Description.ilike("%" + search_text + "%")))

        status = search.get('status')
        if status:
            fil.append(PayRefund.status == int(status))

        items, total_count = await self.paginate_query(fil, PayRefund.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[PayRefund]:
        fil = list()
        fil.append( PayRefund.deleted == 0)
        for k,v in search.items():
            if hasattr(PayRefund,k) and v:
                fil.append(getattr(PayRefund,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( PayRefund.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( PayRefund.status == int(status))
        items = await self.page_fields_nocount_query( PayRefund.get_mini_fields(), fil,  PayRefund.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->PayRefund:
        entity = PayRefund()
        entity.InitInsertEntityWithJson(jsonData)
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->PayRefund:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayRefund=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([PayRefund.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([PayRefund.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[PayRefund],int]:
        fil = list()
        fil.append(PayRefund.creator == self.UserId)
        fil.append(PayRefund.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayRefund.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayRefund.Name.ilike("%" + search_text + "%"))

        status = search.get('status')
        if status:
            fil.append(PayRefund.status == int(status))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, PayRefund.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->PayRefund:
        entity = PayRefund()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.status = 0

        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->PayRefund:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayRefund=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([PayRefund.id==id,PayRefund.creator==self.UserId])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([PayRefund.id.in_(ids),PayRefund.creator==self.UserId])
