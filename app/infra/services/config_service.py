from app.infra.dal.infra_config_dal import InfraConfigDal
from app.system.services.base_service import BaseService


class ConfigService(BaseService):
    async def Get(self,key)->str:
        dal = InfraConfigDal(self.session)
        return await dal.GetByKey(key)