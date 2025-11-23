from sqlalchemy import inspect
from app.system.services.base_service import BaseService
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

class MysqlService(BaseService):    
    async def get_tables(self):
        def _sync_inspect(conn):
            inspector = inspect(conn)  # 对同步连接进行反射
            return inspector.get_table_names()

        try:
            connection = await self.session.connection()
            result = await connection.run_sync(_sync_inspect)
            await self.session.commit()
            return result
        except Exception as e:
            # 记录错误日志
            await self.session.rollback()
            return []
    async def get_table_info(self, table_name):
        def _sync_inspect(conn):
            inspector = inspect(conn)
            if not inspector.has_table(table_name):
                return None
                
            columns = []
            for col in inspector.get_columns(table_name):
                columns.append({'name':col.get('name'),'comment':col.get('comment'),'type':col.get('type')})  # 原字段处理逻辑
                
            return columns  # 返回表信息

        try:
            connection = await self.session.connection()
            result = await connection.run_sync(_sync_inspect)
            await self.session.commit()
            return result
        except Exception as e:
            # 记录错误日志
            await self.session.rollback()
            return None
    
    async def get_table_comment(self, table_name):
        def _sync_inspect(conn):
            inspector = inspect(conn)
            if not inspector.has_table(table_name):
                return None
            comment_info = inspector.get_table_comment(table_name)
            comment = comment_info.get('text', None)
            return comment if comment else table_name

        try:
            connection = await self.session.connection()
            result = await connection.run_sync(_sync_inspect)
            await self.session.commit()
            return result
        except Exception as e:
            await self.session.rollback()
            return None