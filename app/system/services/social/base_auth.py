from abc import ABC, abstractmethod

from app.system.api.types.vo_request import VoSocialAuthRedirect
from app.system.models.system_social_client import SystemSocialClient
from app.system.services.social.auth_enums import AuthSource
from app.system.services.social.auth_token import AuthToken


class BaseAuth(ABC):
    def __init__(self,source:AuthSource,config:SystemSocialClient):
        self.source = source
        self.config:SystemSocialClient = config
        self.access_token = ''
    @abstractmethod
    def get_auth_url(self,state,):
        pass
    @abstractmethod
    async def get_user_info(self, auth_token:VoSocialAuthRedirect):
        pass
    @abstractmethod
    async def user_info_url(self, auth_token:VoSocialAuthRedirect):
        pass