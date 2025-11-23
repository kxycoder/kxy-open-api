from abc import ABC, abstractmethod

from app.system.services.social.auth_token import AuthToken


class BaseAuth(ABC):
    @abstractmethod
    def get_auth_url(self,state,):
        pass
    @abstractmethod
    async def get_user_info(self, auth_token:AuthToken):
        pass
    @abstractmethod
    async def user_info_url(self, auth_token:AuthToken):
        pass