# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import os
import sys
from typing import Dict, List
from app.system.dal.sys_public_dictionary_dal import SysPublicDictionaryDal
from app.config import config
from app.system.models.nodb.message_callback import MessageCallbackModal


class BaseFileService(ABC):
    @abstractmethod
    def __init__(self,access_key,access_key_secret):
        '''初始化'''
        pass
        
    @abstractmethod
    async def uploadFile(self,*args, **kwargs) -> str:
        '''文件上传'''
        pass
