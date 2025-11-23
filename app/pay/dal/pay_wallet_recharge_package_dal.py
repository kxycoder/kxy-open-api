import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.pay.models.pay_wallet_recharge_package import PayWalletRechargePackage
from app.tools import utils
from app.common.basedal import MyBaseDal
from kxy.framework.kxy_logger import KxyLogger

class PayWalletRechargePackageDal(MyBaseDal[PayWalletRechargePackage]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(PayWalletRechargePackage,session,**kwargs)
        self.logger = KxyLogger.getLogger(__name__)

    async def GetByIds(self,ids)->List[PayWalletRechargePackage]:
        return await self.QueryWhere([PayWalletRechargePackage.id.in_(ids)])
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[PayWalletRechargePackage],int]:
        fil = list()
        fil.append(PayWalletRechargePackage.deleted == 0)
        for k,v in search.items():
            if hasattr(PayWalletRechargePackage,k) and v:
                fil.append(getattr(PayWalletRechargePackage,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayWalletRechargePackage.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayWalletRechargePackage.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(PayWalletRechargePackage.DicType.ilike("%" + search_text + "%"),
            #                  PayWalletRechargePackage.Description.ilike("%" + search_text + "%")))

        status = search.get('status')
        if status:
            fil.append(PayWalletRechargePackage.status == int(status))

        items, total_count = await self.paginate_query(fil, PayWalletRechargePackage.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[PayWalletRechargePackage]:
        fil = list()
        fil.append( PayWalletRechargePackage.deleted == 0)
        for k,v in search.items():
            if hasattr(PayWalletRechargePackage,k) and v:
                fil.append(getattr(PayWalletRechargePackage,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( PayWalletRechargePackage.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( PayWalletRechargePackage.status == int(status))
        items = await self.page_fields_nocount_query( PayWalletRechargePackage.get_mini_fields(), fil,  PayWalletRechargePackage.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->PayWalletRechargePackage:
        entity = PayWalletRechargePackage()
        entity.InitInsertEntityWithJson(jsonData)
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->PayWalletRechargePackage:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayWalletRechargePackage=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([PayWalletRechargePackage.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([PayWalletRechargePackage.id.in_(ids)])
 

    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[PayWalletRechargePackage],int]:
        fil = list()
        fil.append(PayWalletRechargePackage.creator == self.UserId)
        fil.append(PayWalletRechargePackage.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PayWalletRechargePackage.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(PayWalletRechargePackage.Name.ilike("%" + search_text + "%"))

        status = search.get('status')
        if status:
            fil.append(PayWalletRechargePackage.status == int(status))

        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, PayWalletRechargePackage.createTime.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonDataUser(self, jsonData)->PayWalletRechargePackage:
        entity = PayWalletRechargePackage()
        entity.InitInsertEntityWithJson(jsonData)
        
        entity.creator=self.UserId
        

        entity.status = 0

        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonDataUser(self,jsonData)->PayWalletRechargePackage:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PayWalletRechargePackage=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.creator = self.UserId
        await self.Update(entity)
        return entity
        
    async def DeleteByUser(self,id):
        await self.DeleteWhere([PayWalletRechargePackage.id==id,PayWalletRechargePackage.creator==self.UserId])


    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([PayWalletRechargePackage.id.in_(ids),PayWalletRechargePackage.creator==self.UserId])
