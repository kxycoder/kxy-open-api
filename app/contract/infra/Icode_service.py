# 接口文件 (基于 code_service.py 生成)

from abc import ABC, abstractmethod


class ICodeService(ABC):
    @abstractmethod
    async def importTables(self, jsonData):
        pass

    @abstractmethod
    async def GenerateByTableIds(self, tableIds, siteUrl='', model=1):
        pass

    @abstractmethod
    async def DeleteOldFile(self, downUrl):
        pass

    @abstractmethod
    async def makeTable(self, tableId):
        pass

    @abstractmethod
    async def GetVarsCacheFirst(self, script, table):
        pass

    @abstractmethod
    async def GenerateByTableId(self, tbleId, fileId=0, batchId =''):
        pass

    @abstractmethod
    async def TestFile(self, fileId):
        pass

    @abstractmethod
    async def GetBaseVars(self, templateId, fileId=0):
        pass

    @abstractmethod
    async def GenerateByFile(self, file, table, baseVar):
        pass

    @abstractmethod
    async def ExcecuteScript(self, cls_str, table, baseVar=None, model='exec'):
        pass

    @abstractmethod
    async def ExcuteByFile(self, file, table, baseVar):
        pass

    @abstractmethod
    async def GetTableDetail(self, tbleId):
        pass

    @abstractmethod
    async def UpdateCodegenTable(self, jsonData):
        pass

    @abstractmethod
    async def CopyTemplate(self, templateId):
        pass

    @abstractmethod
    async def DeleteTemplate(self, templateId):
        pass

