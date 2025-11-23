import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.sys_public_dictionary_type import PublicDictionaryType
from app.tools import utils
from app.common.basedal import BaseDal

class SysPublicDictionaryTypeDal(BaseDal):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(PublicDictionaryType,session,**kwargs)
    
    # 获取列表
    async def Search(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        fil.append(PublicDictionaryType.IsDelete == 0)
        if search.get('SystemCode'):
            fil.append(PublicDictionaryType.SystemCode == search.get('SystemCode'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PublicDictionaryType.Id == int(search_text))
            else:
               search_text =search_text.strip()
               fil.append(or_(PublicDictionaryType.DicType.ilike("%" + search_text + "%"),
                              PublicDictionaryType.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(PublicDictionaryType.Status == int(status))
        items, total_count = await self.paginate_query(fil, PublicDictionaryType.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        fil.append(PublicDictionaryType.UID == self.UserId)
        fil.append(PublicDictionaryType.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(PublicDictionaryType.Id == int(search_text))
            else:
               search_text =search_text.strip()
               fil.append(or_(PublicDictionaryType.DicType.ilike("%" + search_text + "%"),
                              PublicDictionaryType.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(PublicDictionaryType.Status == int(status))
        items, total_count = await self.paginate_query(fil, PublicDictionaryType.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def GetByDicType(self,DicType)->PublicDictionaryType:
        return await self.QueryOne([PublicDictionaryType.DicType==DicType,PublicDictionaryType.IsDelete==0])
    async def AddByJsonData(self, jsonData)->PublicDictionaryType:
        entity = PublicDictionaryType()
        entity.InitInsertEntityWithJson(jsonData)    
        exist = await self.GetByDicType(entity.DicType)
        if exist:
            await self.Rollback()
            raise FriendlyException(f'字典类型{entity.DicType}已存在')
        entity.Status = 1
        entity.IsDelete = 0
        entity.CanEdit = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->PublicDictionaryType:
        entity = PublicDictionaryType()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->PublicDictionaryType:
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PublicDictionaryType=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->PublicDictionaryType:
        '''更新客户自己的数据'''
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:PublicDictionaryType=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.UpdateFields([PublicDictionaryType.Id==id],{'IsDelete':1})

    async def DeleteByUser(self,id):
        await self.UpdateFields([PublicDictionaryType.Id==id,PublicDictionaryType.UID==self.UserId],{'IsDelete':1})

    async def get_user_editable_types(self,systemcode: str = None)-> list[PublicDictionaryType]:
        """
        获取当前用户可编辑的public_dictionary字典类型（CanEdit=1，未删除，激活状态）
        """
        from app.system.models.sys_public_dictionary_type import PublicDictionaryType
        fil = [
            PublicDictionaryType.SystemCode == systemcode,
            PublicDictionaryType.CanEdit == 1,
            PublicDictionaryType.IsDelete == 0,
            PublicDictionaryType.Status == 1
        ]
        return await self.QueryWhere(fil)
