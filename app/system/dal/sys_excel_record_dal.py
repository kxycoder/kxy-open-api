import re
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.sys_excel_record import ExcelRecord
from app.tools import utils
from app.common.basedal import BaseDal

class SysExcelRecordDal(BaseDal[ExcelRecord]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(ExcelRecord,session,**kwargs)
    
    # 获取列表
    async def Search(self,search,page_index, page_size)->tuple[List[ExcelRecord],int]:
        fil = list()
        fil.append(ExcelRecord.IsDelete == 0)
        search_text=search.get('search')
        roles = search.get('roles', [])
        if 'admin' not in roles:
            fil.append(ExcelRecord.CreateUser == self.UserId)
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ExcelRecord.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ExcelRecord.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(ExcelRecord.DicType.ilike("%" + search_text + "%"),
            #                  ExcelRecord.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(ExcelRecord.Status == int(status))
        items, total_count = await self.paginate_query(fil, ExcelRecord.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        fil.append(ExcelRecord.UID == self.UserId)
        fil.append(ExcelRecord.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ExcelRecord.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ExcelRecord.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(ExcelRecord.Status == int(status))
        items, total_count = await self.paginate_query(fil, ExcelRecord.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonData(self, jsonData)->ExcelRecord:
        entity = ExcelRecord()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->ExcelRecord:
        entity = ExcelRecord()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->ExcelRecord:
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ExcelRecord=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->ExcelRecord:
        '''更新客户自己的数据'''
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ExcelRecord=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.UpdateFields([ExcelRecord.Id==id],{'IsDelete':1})

    async def DeleteByUser(self,id):
        await self.UpdateFields([ExcelRecord.Id==id,ExcelRecord.UID==self.UserId],{'IsDelete':1})
    async def Add(self,tableName,pageName,action):
        entity = ExcelRecord()
        entity.TableName = tableName
        entity.PageName = pageName
        entity.Status = 5
        entity.Action  = action
        entity.ExcelFile = ''
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity