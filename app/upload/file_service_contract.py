# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
class BaseFileService(ABC):
    @abstractmethod
    def __init__(self,access_key,access_key_secret):
        '''初始化'''
        pass
        
    @abstractmethod
    async def uploadFile(self,*args, **kwargs) -> str:
        '''文件上传'''
        pass
