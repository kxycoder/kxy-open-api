# 接口文件 (基于 excel_service.py 生成)

from abc import ABC, abstractmethod


class IExcelService(ABC):
    @abstractmethod
    async def AddSetting(self, jsonData):
        pass

    @abstractmethod
    async def ExportExcel(self, modal, dal, *args, **kwargs):
        pass

    @abstractmethod
    async def _exportExcel(self, exportId, setting, dal, fields, *args, **kwargs):
        pass

    @abstractmethod
    async def UpdateSetting(self, jsonData):
        pass

    @abstractmethod
    async def DeleteSetting(self, id):
        pass

