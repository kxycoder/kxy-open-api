import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.pay.models.pay_wallet_recharge import PayWalletRecharge
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class PayWalletRechargeDal(MyBaseDal[PayWalletRecharge]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(PayWalletRecharge,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[PayWalletRecharge]:
        return await self.QueryWhere([PayWalletRecharge.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[PayWalletRecharge],int]:
        fil = list()
        fil.append(PayWalletRecharge.deleted == 0)
        for k,v in search.items():
            if hasattr(PayWalletRecharge,k) and v:
                fil.append(getattr(PayWalletRecharge,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayWalletRecharge.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayWalletRecharge.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(PayWalletRecharge.DicType.ilike("%" + search_text + "%"),
            #                  PayWalletRecharge.Description.ilike("%" + search_text + "%")))

        items, total_count = await self.paginate_query(fil, PayWalletRecharge.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[PayWalletRecharge]:
        fil = list()
        fil.append( PayWalletRecharge.deleted == 0)
        for k,v in search.items():
            if hasattr(PayWalletRecharge,k) and v:
                fil.append(getattr(PayWalletRecharge,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( PayWalletRecharge.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( PayWalletRecharge. == int(status))
        items = await self.page_fields_nocount_query( PayWalletRecharge.get_mini_fields(), fil,  PayWalletRecharge.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->PayWalletRecharge:
        entity = PayWalletRecharge()
        entity.InitInsertEntityWithJson(jsonData)
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->PayWalletRecharge:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayWalletRecharge=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([PayWalletRecharge.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([PayWalletRecharge.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[PayWalletRecharge],int]:
        fil = list()
        fil.append(PayWalletRecharge.creator == self.UserId)
        fil.append(PayWalletRecharge.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayWalletRecharge.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayWalletRecharge.Name.ilike("%" + search_text + "%"))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, PayWalletRecharge.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->PayWalletRecharge:
        entity = PayWalletRecharge()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->PayWalletRecharge:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayWalletRecharge=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([PayWalletRecharge.id==id,PayWalletRecharge.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([PayWalletRecharge.id.in_(ids),PayWalletRecharge.creator==self.UserId])
