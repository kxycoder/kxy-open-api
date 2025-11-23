import re
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.sys_excel_setting_detail import ExcelSettingDetail
from app.tools import utils
from app.common.basedal import BaseDal

class SysExcelSettingDetailDal(BaseDal[ExcelSettingDetail]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(ExcelSettingDetail,session,**kwargs)
    
    # 获取列表
    async def Search(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        fil.append(ExcelSettingDetail.IsDelete == 0)
        search_text=search.get('search')
        SettingId = search.get('SettingId')
        if SettingId:
            fil.append(ExcelSettingDetail.SettingId == SettingId)
        else:
            return [],0
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ExcelSettingDetail.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ExcelSettingDetail.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(ExcelSettingDetail.DicType.ilike("%" + search_text + "%"),
            #                  ExcelSettingDetail.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(ExcelSettingDetail.Status == int(status))
        items, total_count = await self.paginate_query(fil, ExcelSettingDetail.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search,page_index, page_size)->tuple[Sequence,int]:
        fil = list()
        fil.append(ExcelSettingDetail.UID == self.UserId)
        fil.append(ExcelSettingDetail.IsDelete == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(ExcelSettingDetail.Id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(ExcelSettingDetail.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(ExcelSettingDetail.Status == int(status))
        items, total_count = await self.paginate_query(fil, ExcelSettingDetail.CreateDate.desc(), page_index, page_size)
        return items, total_count
    async def AddByJsonData(self, jsonData)->ExcelSettingDetail:
        entity = ExcelSettingDetail()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->ExcelSettingDetail:
        entity = ExcelSettingDetail()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.Status = 1
        entity.IsDelete = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->ExcelSettingDetail:
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ExcelSettingDetail=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->ExcelSettingDetail:
        '''更新客户自己的数据'''
        id=jsonData.get('Id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:ExcelSettingDetail=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.UpdateFields([ExcelSettingDetail.Id==id],{'IsDelete':1})

    async def DeleteByUser(self,id):
        await self.UpdateFields([ExcelSettingDetail.Id==id,ExcelSettingDetail.UID==self.UserId],{'IsDelete':1})
    async def AddFields(self,Id,canExport,canImport,colums):
        cretorFields = ['CreateUserName','CreateUser','CreateDate','LastModifiedUser','LastModifiedDate']
        for col in colums:
            colName = col.get('name')
            if not colName or colName in cretorFields:
                continue
            entity = ExcelSettingDetail()
            entity.SettingId = Id
            entity.FieldName = colName
            entity.CanExport = canExport
            entity.CanImport = canImport
            comment = col.get('comment',colName)
            entity.ExcelFieldName =comment if comment else colName
            entity.FieldType = col.get('type','string')
            entity.IsDelete = 0
            await self.Insert(entity)
    async def GetBySettingId(self,Id)->List[ExcelSettingDetail]:
        return await self.QueryWhere([ExcelSettingDetail.SettingId==Id, ExcelSettingDetail.IsDelete==0])

    async def GetCanExportFields(self,Id)->List[ExcelSettingDetail]:
        return await self.QueryWhere([ExcelSettingDetail.SettingId==Id, ExcelSettingDetail.CanExport==1,ExcelSettingDetail.IsDelete==0])

    async def GetCanImportFields(self,Id)->List[ExcelSettingDetail]:
        return await self.QueryWhere([ExcelSettingDetail.SettingId==Id, ExcelSettingDetail.CanImport==1,ExcelSettingDetail.IsDelete==0])
        
    async def UpdateAction(self,Id,CanImport,CanExport):
        details = await self.GetBySettingId(Id)
        if not details:
            return
        for detail in details:
            detail.CanImport = CanImport
            detail.CanExport = CanExport
            await self.Update(detail)
    async def DeleteBySettingId(self,Id):
        await self.UpdateFields([ExcelSettingDetail.SettingId==Id],{'IsDelete':1})
        # 这里不需要返回值，直接删除即可
        # return True