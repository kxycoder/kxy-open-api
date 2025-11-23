import asyncio
from datetime import datetime
from io import BytesIO
import os
from typing import List
import uuid
import zipfile

from openpyxl import Workbook
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.sys_excel_record import ExcelRecord
from app.system.dal.sys_excel_setting_dal import SysExcelSettingDal
from app.system.dal.sys_excel_setting_detail_dal import SysExcelSettingDetailDal
from app.system.models.sys_excel_setting import ExcelSetting
from app.system.models.sys_excel_setting_detail import ExcelSettingDetail
from app.system.services.base_service import BaseService
from app.system.dal.sys_excel_record_dal  import SysExcelRecordDal
from kxy.framework.mapper import Mapper
from app.database import AsyncSessionLocal

class ExcelService(BaseService):
    async def AddSetting(self,jsonData):
        tableName = jsonData.get('TableName')
        if not tableName:
            raise FriendlyException('请选择表')
        mysqlService = Mapper.getservice('MysqlService',self.session)
        colums =await mysqlService.get_table_info(tableName)
        # get_table_comment
        jsonData['TableDescription'] = await mysqlService.get_table_comment(tableName)
        setting =  await SysExcelSettingDal(self.session).AddByJsonData(jsonData)
        await SysExcelSettingDetailDal(self.session).AddFields(setting.Id,setting.CanExport,setting.CanImport,colums)
        return setting
        
    async def ExportExcel(self,modal,dal,*args,**kwargs):
        setting = await SysExcelSettingDal(self.session).GetByTableName(modal.__tablename__)
        if not setting or not setting.CanExport:
            raise FriendlyException('禁止导出')
        details = await SysExcelSettingDetailDal(self.session).GetCanExportFields(setting.Id)
        recorDal = SysExcelRecordDal(self.session)
        entity = await recorDal.Add(setting.TableName,setting.TableDescription,"导出")
        asyncio.create_task(self._exportExcel(entity.Id,setting,dal,details,*args,**kwargs))

    async def _exportExcel(self,exportId,setting:ExcelSetting,dal,fields:List[ExcelSettingDetail],*args,**kwargs):
        async with AsyncSessionLocal() as session:
            recorDal = SysExcelRecordDal(session)
            entity = await recorDal.GetExist(exportId)
            try:
                recorDal.AddLogger('导出Excel',f'查询条件:{args}')
                # 创建Excel文件（内存中）
                output = BytesIO()
                workbook = Workbook()
                workbook.encoding = 'utf-8'
                worksheet = workbook.active
                
                # 写入表头
                headers = [f.ExcelFieldName for f in fields]
                worksheet.append(headers)
                kwargs['page_size'] = 100
                pageIndex=1
                search_func = dal(session)
                while True:
                    kwargs['page_index'] = pageIndex
                    datas,total =await search_func.Search(*args,**kwargs)
                    # 写入数据行
                    for row in datas:
                        # 只导出指定字段
                        worksheet.append([getattr(row, field.FieldName, '') for field in fields])
                    if len(datas)==0 or len(datas)<total:
                        break
                    pageIndex+=1
                # 生成文件夹路径 年/月/日
                now = datetime.now()
                dir_path = os.path.join(
                    "./export_excels",
                    str(now.year),
                    str(now.month).zfill(2),
                    str(now.day).zfill(2)
                )
                os.makedirs(dir_path, exist_ok=True)
                file_uuid = uuid.uuid4().hex
                excel_file_name = f"{file_uuid}.xlsx"
                excel_file_path = os.path.join(dir_path, excel_file_name)
                workbook.save(excel_file_path)

                # 压缩为zip文件
                zip_file_name = f"{file_uuid}.zip"
                zip_file_path = os.path.join(dir_path, zip_file_name)
                with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(excel_file_path, arcname=excel_file_name)

                # 可选：删除原始excel文件
                os.remove(excel_file_path)

                # 写入zip文件路径到entity
                entity.ExcelFile = zip_file_path.replace('./export_excels/', '')
                entity.Status = 10  # 标记导出成功
                await recorDal.Update(entity)
            except Exception as e:
                entity.Status= 4
                entity.Remark = str(e)
                await recorDal.Update(entity)
            
    async def UpdateSetting(self,jsonData):
        setting = await SysExcelSettingDal(self.session).Get(jsonData.get('Id'))
        excelDetailDal = SysExcelSettingDetailDal(self.session)
        if not setting:
            raise FriendlyException('设置不存在')
        setting.InitUpdateFiles(jsonData)
        await excelDetailDal.UpdateAction(setting.Id,setting.CanImport,setting.CanExport)
        await SysExcelSettingDal(self.session).Update(setting)
        return setting
    async def DeleteSetting(self,id):
        setting = await SysExcelSettingDal(self.session).Get(id)
        if not setting:
            raise FriendlyException('设置不存在')
        await SysExcelSettingDetailDal(self.session).DeleteBySettingId(id)
        await SysExcelSettingDal(self.session).Delete(id)
        return True
        