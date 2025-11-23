import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_social_client import SystemSocialClient
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemSocialClientDal(MyBaseDal[SystemSocialClient]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemSocialClient,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemSocialClient],int]:
        fil = list()
        fil.append(SystemSocialClient.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemSocialClient,k) and v:
                fil.append(getattr(SystemSocialClient,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemSocialClient.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemSocialClient.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemSocialClient.DicType.ilike("%" + search_text + "%"),
            #                  SystemSocialClient.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemSocialClient.status == int(status))
        items, total_count = await self.paginate_query(fil, SystemSocialClient.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemSocialClient],int]:
        fil = list()
        fil.append(SystemSocialClient.UID == self.UserId)
        fil.append(SystemSocialClient.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemSocialClient.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemSocialClient.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemSocialClient.status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemSocialClient.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemSocialClient]:
        fil = list()
        fil.append( SystemSocialClient.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemSocialClient,k) and v:
                fil.append(getattr(SystemSocialClient,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemSocialClient.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemSocialClient.status == int(status))
        items = await self.page_fields_nocount_query( SystemSocialClient.get_mini_fields(), fil,  SystemSocialClient.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->SystemSocialClient:
        entity = SystemSocialClient()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemSocialClient:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemSocialClient=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity
    async def Delete(self,id):
        await self.DeleteWhere([SystemSocialClient.id==id])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemSocialClient.id.in_(ids)])

    async def GetBySocialType(self,type):
        return await self.QueryOne([SystemSocialClient.socialType==type,SystemSocialClient.status==0,SystemSocialClient.deleted==0])
