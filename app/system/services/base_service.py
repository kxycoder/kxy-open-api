from sqlalchemy.ext.asyncio import AsyncSession
from kxy.framework.context import user_id,user_info,current_tenant_id
from app.tools import utils
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)
class BaseService():
    def __init__(self,session:AsyncSession,**kwargs):
        self.session = session
        self.user_id = kwargs.get('UserId',user_id.get())
        self.user_name = kwargs.get('UserName',user_info.get().get('chineseName',''))
        self.tenantId = current_tenant_id.get()
        self.logger = logger