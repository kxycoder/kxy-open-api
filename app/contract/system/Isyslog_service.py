# 接口文件 (基于 syslog_service.py 生成)

from abc import ABC, abstractmethod


class IBatchSysLogService(ABC):
    @abstractmethod
    async def _background_task(self):
        pass

    @abstractmethod
    async def AddLogAsync(self, tableName, action, data):
        pass

    @abstractmethod
    async def flush(self):
        pass

    @abstractmethod
    async def _addBatchLog(self, logs):
        pass

