import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.sys_excel_setting import ExcelSetting
from app.tools import utils
from app.common.basedal import BaseDal

class SysExcelSettingDal(BaseDal[ExcelSetting]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(ExcelSetting,session,**kwargs)
    
    # 获取列表
    async def Search(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        fil.append(ExcelSetting.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ExcelSetting.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ExcelSetting.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(ExcelSetting.DicType.ilike("%" + search_text + "%"),
            #                  ExcelSetting.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(ExcelSetting.Status == int(status))
        items, total_count = await self.paginate_query(fil, ExcelSetting.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        fil.append(ExcelSetting.UID == self.UserId)
        fil.append(ExcelSetting.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ExcelSetting.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ExcelSetting.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(ExcelSetting.Status == int(status))
        items, total_count = await self.paginate_query(fil, ExcelSetting.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonData(self, jsonData)->ExcelSetting:
        table_name = jsonData.get('TableName')
        if table_name:
            exist = await self.QueryOne([ExcelSetting.TableName == table_name, ExcelSetting.IsDelete == 0])
            if exist:
                raise FriendlyException(f"表名为 {table_name} 的数据已存在")
        entity = ExcelSetting()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.DataBase='kxy'
        entity.ProcessModule = ''
        entity.TemplateFile = ''
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->ExcelSetting:
        entity = ExcelSetting()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.DataBase='kxy'
        entity.ProcessModule = ''
        entity.TemplateFile = ''
        entity.Status = 1
        entity.IsDelete = 0
        entity.CanExport = 0
        entity.CanImport = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->ExcelSetting:
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ExcelSetting=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->ExcelSetting:
        '''更新客户自己的数据'''
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ExcelSetting=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.UpdateFields([ExcelSetting.Id==id],{'IsDelete':1})

    async def DeleteByUser(self,id):
        await self.UpdateFields([ExcelSetting.Id==id,ExcelSetting.UID==self.UserId],{'IsDelete':1})
    async def GetByTableName(self,tableName):
        return await self.QueryOne([ExcelSetting.TableName==tableName,ExcelSetting.IsDelete==0])