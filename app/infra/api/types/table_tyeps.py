# file: app/infra/api/types/table_import_request.py

from typing import Optional, Dict, Any
from pydantic import BaseModel

class TableImportRequest(BaseModel):
    """
    表导入请求参数
    """
    script: str  # 脚本内容
    databaseName: str  # 数据库名称
    templateId: int  # 模板ID
    templateParam: Optional[Dict[str, Any]] = None  # 模板参数