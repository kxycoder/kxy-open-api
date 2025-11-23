import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.pay.models.pay_demo_transfer import PayDemoTransfer
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class PayDemoTransferDal(MyBaseDal[PayDemoTransfer]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(PayDemoTransfer,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[PayDemoTransfer]:
        return await self.QueryWhere([PayDemoTransfer.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[PayDemoTransfer],int]:
        fil = list()
        fil.append(PayDemoTransfer.deleted == 0)
        for k,v in search.items():
            if hasattr(PayDemoTransfer,k) and v:
                fil.append(getattr(PayDemoTransfer,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayDemoTransfer.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayDemoTransfer.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(PayDemoTransfer.DicType.ilike("%" + search_text + "%"),
            #                  PayDemoTransfer.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, PayDemoTransfer.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[PayDemoTransfer]:
        fil = list()
        fil.append( PayDemoTransfer.deleted == 0)
        for k,v in search.items():
            if hasattr(PayDemoTransfer,k) and v:
                fil.append(getattr(PayDemoTransfer,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( PayDemoTransfer.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( PayDemoTransfer. == int(status))
        items = await self.page_fields_nocount_query( PayDemoTransfer.get_mini_fields(), fil,  PayDemoTransfer.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->PayDemoTransfer:
        entity = PayDemoTransfer()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->PayDemoTransfer:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayDemoTransfer=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([PayDemoTransfer.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([PayDemoTransfer.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[PayDemoTransfer],int]:
        fil = list()
        fil.append(PayDemoTransfer.creator == self.UserId)
        fil.append(PayDemoTransfer.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayDemoTransfer.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayDemoTransfer.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, PayDemoTransfer.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->PayDemoTransfer:
        entity = PayDemoTransfer()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->PayDemoTransfer:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayDemoTransfer=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([PayDemoTransfer.id==id,PayDemoTransfer.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([PayDemoTransfer.id.in_(ids),PayDemoTransfer.creator==self.UserId])
