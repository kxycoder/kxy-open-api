from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class DepartmentStandard:
    """标准化的部门信息实体."""

    id: Any
    name: str
    parentId: Any = None
    leader: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """以统一结构输出字典形式."""
        data = asdict(self)
        data["leader"] = data.get("leader") or ""
        return data
