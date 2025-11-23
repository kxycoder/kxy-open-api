# -*- coding: utf-8 -*-

import json
import os
import sys
from typing import Dict, List
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525.client import Client as Client
from alibabacloud_dysmsapi20170525 import models as models
from Tea.exceptions import UnretryableException,TeaException
from app.contract.types.send_types import SenderReturnModal,MessageCallbackModal
from alibabacloud_dysmsapi20170525.models import AddSmsTemplateRequest
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from app.global_var import SmsTempalteTypes
from app.sms.sms_sender import SMSSender
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

class ALiyunSender(SMSSender):
    def __init__(self,access_key,access_key_secret,signature):
        super().__init__(access_key,access_key_secret,signature)
        config = open_api_models.Config(
            access_key_id=access_key,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'dysmsapi.aliyuncs.com'
        self.client = Client(config)
    
    async def send_message(self,phone_number:str,templateCode:str,templateParams:Dict[str,str],*args, **kwargs) -> str:
        request = models.SendSmsRequest()
        request.phone_numbers = phone_number
        request.sign_name = self.signature
        request.template_code = templateCode
        request.template_param = json.dumps(templateParams)
        
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = await self.client.send_sms_async(request)
            request_id = response.body.biz_id
            if not request_id:
                logger.error(f'发送短信失败:{phone_number},{templateCode},{templateParams},{response.body.message}')
                raise Exception(f'发送短信失败:{phone_number},{templateCode},{templateParams},{response.body.message}')
            return SenderReturnModal(
                code = response.body.code,
                message = response.body.message,
                requestId = response.body.request_id,
                serialNo = response.body.biz_id,
            )
        except UnretryableException as e:
            # 网络异常
            logger.error(f'发送短信时网络异常:{e},参数：{phone_number},{templateCode},{templateParams}')
            raise e
        except TeaException as e:
            # 业务异常
            logger.error(f'发送短信时业务异常:{e},参数：{phone_number},{templateCode},{templateParams}')
            raise e
        except Exception as e:
            logger.error(f'发送短信时其他异常:{e},参数：{phone_number},{templateCode},{templateParams}')
            raise e
    async def callBack(self,*args, **kwargs) -> List[MessageCallbackModal]:
        # [{"send_time": "2017-08-30 00:00:00", "report_time": "2017-08-30 00:00:00", "success": true, "err_msg": "用户接收成功", "err_code": "DELIVERED", "phone_number": "18612345678", "sms_size": "1", "biz_id": "932702304080415357^0", "out_id": "1184585343"}]
        # [{"send_time": "2025-06-28 12:30:01", "report_time": "2025-06-28 12:30:53", "success": false, "err_msg": "签名实名制报备问题。应运营商要求，各短信发送通道需完成对应签名的实名制报备。", "err_code": "PORT_NOT_REGISTERED", "phone_number": "18616541211", "sms_size": "1", "biz_id": "177503851085001567^0"}]
        jsonData = args[0]
        results = []
        for data in jsonData:
            modal = MessageCallbackModal(requestId=data.get('biz_id'),**data)
            results.append(modal)
        return results
    async def translateTemplateType(self,types:SmsTempalteTypes):
        return {
            SmsTempalteTypes.Verify: 0,
            SmsTempalteTypes.Notice: 1,
            SmsTempalteTypes.Marketing: 2
        }.get(types)
    
    async def addTemplate(self,templateName:str,templateContent:str,templateType:SmsTempalteTypes,remark,**kwargs) -> str:
        # https://next.api.aliyun.com/api-tools/sdk/Dysmsapi?spm=a2c4g.11186623.0.0.239a74b8ppPp5S&version=2017-05-25&language=python-tea&tab=sdk-demo
        request = AddSmsTemplateRequest()
        # 设置模板名称
        request.template_name = templateName
        # 设置模板内容
        request.template_content = templateContent
        # 设置模板类型（0:验证码 1:短信通知 2:推广短信 3:国际/港澳台消息）
        request.template_type = self.translateTemplateType(templateType)
        # 场景说明，便于审核
        request.remark = remark
        
        try:
            # 调用添加模板接口
            response = await self.client.add_sms_template_async(request)
            # 返回模板CODE
            return response.body.template_code
        #   {
        #     "TemplateCode": "SMS_16703****",
        #     "Message": "OK",
        #     "RequestId": "0A974B78-02BF-4C79-ADF3-90CFBA1B55B1",
        #     "TemplateContent": "亲爱的会员！阿里云短信服务祝您新年快乐！",
        #     "TemplateName": "阿里云短信测试模板",
        #     "TemplateType": "1",
        #     "CreateDate": "2019-06-04 11:42:17",
        #     "Code": "OK",
        #     "Reason": "无审批备注",
        #     "TemplateStatus": "1"
        # }
        except Exception as e:
            logger.error(f"创建短信模板失败: {e}")
            raise e
    async def updateTemplate(self,templateCode,templateName:str,templateContent:str,templateType:SmsTempalteTypes,remark,**kwargs):
        request = dysmsapi_20170525_models.UpdateSmsTemplateRequest()
        request.template_name = templateName
        request.template_content = templateContent
        request.template_type = self.translateTemplateType(templateType)
        request.template_code = templateCode
        request.remark = remark
        runtime = util_models.RuntimeOptions()
        try:
            await self.client.update_sms_template_with_options_async(request, runtime)
        except Exception as error:
            raise error.message