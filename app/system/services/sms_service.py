from datetime import datetime
from typing import Dict
from app.contract.system.Iuser_service import IUserService
from app.global_var import ReciveStatus, SendStatus, SmsTempalteTypes
from app.sms.aliyun_sender import ALiyunSender
from app.sms.sms_sender import SMSSender
from app.system.dal.system_sms_log_dal import SystemSmsLogDal
from app.system.dal.system_sms_template_dal import SystemSmsTemplateDal
from app.system.dal.system_sms_channel_dal import SystemSmsChannelDal
from app.system.models.system_sms_channel import SystemSmsChannel
from app.system.models.system_sms_log import SystemSmsLog
from app.system.models.system_users import SystemUsers
from app.system.services.base_service import BaseService
from kxy.framework.friendly_exception import FriendlyException
from app.tools import utils
from kxy.framework.mapper import Mapper

channel_dict:Dict[int,SystemSmsChannel] = {}
class SmsService(BaseService):
    async def SendByUserId(self,userid, templateCode,**params):
        svc = Mapper.getservice_by_contract(IUserService,self.session)
        user:SystemUsers = await svc.GetUserById(userid)
        return await self.SendByDetail(user.id,1,user.mobile,templateCode,**params)
    async def SendByDetail(self,userId,userType,mobile,templateCode,**params):
        sendLog =await self.GenerateLog(templateCode,userId,userType,mobile,**params)
        return await self.SendByLog(sendLog)
    async def createClient(self,channelInfo:SystemSmsChannel)->SMSSender:
        if channelInfo.code =='ALIYUN':
            return ALiyunSender(channelInfo.apiKey,channelInfo.apiSecret,channelInfo.signature)
        else:
            raise FriendlyException(f'暂不支持此渠道{channelInfo.code}-{channelInfo.signature}')
    async def GetSender(self,channelId:int):
        sender = channel_dict.get(channelId)
        if not sender:
            channel = SystemSmsChannelDal(self.session)
            channelInfo = await channel.GetExist(channelId)
            sender = await self.createClient(channelInfo)
        return sender
    async def SendByLog(self,sendLog:SystemSmsLog):
        logDal = SystemSmsLogDal(self.session)
        try:
            sender = await self.GetSender(sendLog.channelId)
            result = await sender.send_message(sendLog.mobile,sendLog.apiTemplateId,sendLog.templateParams)
            sendLog.sendStatus = SendStatus.Success.value
            sendLog.sendTime = datetime.now()
            sendLog.apiSerialNo = result.serialNo
            sendLog.apiSendCode = result.code
            sendLog.apiSendMsg = result.message
            sendLog.apiRequestId = result.requestId
            await logDal.Insert(sendLog)
        except Exception as e:
            sendLog.sendStatus = SendStatus.Fail.value
            sendLog.receiveStatus = SendStatus.Fail.value
            sendLog.apiSendMsg = str(e)
            await logDal.Insert(sendLog)
            raise e
    async def GenerateLog(self,templateCode,userId,userType,mobile,**params):
        dal = SystemSmsTemplateDal(self.session)
        template = await dal.GetByCode(templateCode)
        if not template:
            raise FriendlyException('模版不存在')
        sms = SystemSmsLog()
        sms.channelId = template.channelId
        sms.channelCode = template.channelCode
        sms.templateId = template.id
        sms.templateCode = template.code
        sms.templateType = template.type
        sms.templateContent = utils.replace_str_params(template.content,**params)
        sms.templateParams = params
        sms.apiTemplateId = template.apiTemplateId
        sms.mobile = mobile
        sms.userId = userId
        sms.userType = userType
        sms.sendStatus = SendStatus.Create.value
        sms.receiveStatus = ReciveStatus.Waite.value
        return sms
    async def AddTemplate(self,jsonData):
        channel = await SystemSmsChannelDal(self.session).Get(jsonData.get('channelId'))
        jsonData['channelCode'] = channel.code
        sender = await self.createClient(channel)
        template = await SystemSmsTemplateDal(self.session).AddByJsonData(jsonData)
        await sender.addTemplate(template.name,template.content,SmsTempalteTypes(template.type),template.remark)
        return template
    async def UpdateTemplate(self,jsonData):
        template = await SystemSmsTemplateDal(self.session).UpdateByJsonData(jsonData)
        sender = await self.createClient(template.channelId)
        await sender.updateTemplate(template.apiTemplateId,template.name,template.content,SmsTempalteTypes(template.type),template.remark)