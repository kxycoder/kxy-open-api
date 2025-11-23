# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import os
import sys
from typing import Dict, List
from app.contract.types.send_types import SenderReturnModal,MessageCallbackModal
from app.global_var import SmsTempalteTypes


class SMSSender(ABC):
    def __init__(self,access_key,access_key_secret,signature):
        '''初始化'''
        self.access_key = access_key
        self.access_key_secret = access_key_secret
        self.signature = signature
        
    @abstractmethod
    async def send_message(self,phone_number:str,templateCode:str,templateParams:Dict[str,str],*args, **kwargs) -> SenderReturnModal:
        '''短信发送'''
        pass
    
    @abstractmethod
    async def callBack(self,*args, **kwargs) -> List[MessageCallbackModal]:
        '''短信发送回执回调'''
        pass
    @abstractmethod
    async def addTemplate(self,templateName:str,templateContent:str,templateType:SmsTempalteTypes,remark,**kwargs):
        '''添加短信模板'''
        pass
    @abstractmethod
    async def updateTemplate(self,templateCode,templateName:str,templateContent:str,templateType:SmsTempalteTypes,remark,**kwargs):
        '''修改短信模板'''
        pass