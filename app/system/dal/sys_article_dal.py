import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.sys_article import SysArticle
from app.tools import utils
from app.common.basedal import BaseDal


class SysArticleDal(BaseDal[SysArticle]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__(SysArticle,db,**kwargs)
    
    # 获取列表
    async def Search(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        fil.append(SysArticle.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SysArticle.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SysArticle.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SysArticle.Status == int(status))
        items, total_count = await self.paginate_query( fil, SysArticle.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        # fil.append(SysArticle.UID == self.UserId)
        fil.append(SysArticle.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SysArticle.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SysArticle.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SysArticle.Status == int(status))
        items, total_count = await self.paginate_query( fil, SysArticle.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonData(self, jsonData)->SysArticle:
        entity = SysArticle()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SysArticle:
        entity = SysArticle()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SysArticle:
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SysArticle=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SysArticle:
        '''更新客户自己的数据'''
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SysArticle=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.UpdateFields([SysArticle.Id==id],{'IsDelete':1})

    async def DeleteByUser(self,id):
        await self.UpdateFields([SysArticle.Id==id,SysArticle.UID==self.UserId],{'IsDelete':1})
