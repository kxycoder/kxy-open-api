import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.infra.models.infra_file_content import InfraFileContent
from app.tools import utils

from app.common.basedal import MyBaseDal

class InfraFileContentDal(MyBaseDal[InfraFileContent]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(InfraFileContent,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[InfraFileContent],int]:
        fil = list()
        fil.append(InfraFileContent.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraFileContent,k) and v:
                fil.append(getattr(InfraFileContent,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(InfraFileContent.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(InfraFileContent.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(InfraFileContent.DicType.ilike("%" + search_text + "%"),
            #                  InfraFileContent.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(InfraFileContent.Status == int(status))
        items, total_count = await self.paginate_query(fil, InfraFileContent.createTime.desc(), page_index, page_size)
        return items, total_count


    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[InfraFileContent]:
        fil = list()
        fil.append( InfraFileContent.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraFileContent,k) and v:
                fil.append(getattr(InfraFileContent,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( InfraFileContent.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( InfraFileContent.Status == int(status))
        items = await self.page_fields_nocount_query( InfraFileContent.get_mini_fields(), fil,  InfraFileContent.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->InfraFileContent:
        entity = InfraFileContent()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity


    async def UpdateByJsonData(self,jsonData)->InfraFileContent:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:InfraFileContent=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity



    async def Delete(self,id):
        await self.DeleteWhere([InfraFileContent.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([InfraFileContent.id.in_(ids)])

