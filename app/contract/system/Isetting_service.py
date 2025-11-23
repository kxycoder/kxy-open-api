# 接口文件 (基于 setting_service.py 生成)

from abc import ABC, abstractmethod


class ISettingService(ABC):
    @abstractmethod
    async def get_user_editable_public_dictionary_types(self, systemcode=None):
        pass

