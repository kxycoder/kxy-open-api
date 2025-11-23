# 接口文件 (基于 mysql_service.py 生成)

from abc import ABC, abstractmethod


class IMysqlService(ABC):
    @abstractmethod
    async def get_tables(self):
        pass

    @abstractmethod
    async def _sync_inspect(conn):
        pass

    @abstractmethod
    async def get_table_info(self, table_name):
        pass

    @abstractmethod
    async def _sync_inspect(conn):
        pass

    @abstractmethod
    async def get_table_comment(self, table_name):
        pass

    @abstractmethod
    async def _sync_inspect(conn):
        pass

