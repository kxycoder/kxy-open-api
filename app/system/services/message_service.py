# -*- coding: utf-8 -*-

import asyncio
from datetime import date, datetime, timedelta
import json
import requests
from sqlalchemy.ext.asyncio import AsyncSession
from kxy.framework.friendly_exception import FriendlyException
from app.system.dal.message_send_setting_dal import MessageSendSettingDal
from app.system.dal.message_send_record_dal import MessageSendRecordDal
from app.system.dal.sys_message_dal import SysMessageDal
from app.system.dal.sys_user_extend_dal import SysUserExtendDal
from app.system.models.message_send_setting import MessageSendSetting
from app.system.services.base_service import BaseService
from app.system.dal.sys_public_dictionary_dal import SysPublicDictionaryDal
from app.system.dal.sys_users_dal import SysUsersDal
from app.system.models.sys_users import SysUsers
from app.config import config
from app.sms.aliyun_sender import ALiyunSender
from app.sms.sms_sender import SMSSender
from app.tools import utils
from app.global_var import MsgTypes, SendStatus, SendTypes
from lunardate import LunarDate
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)

class MessageService(BaseService):
    client:SMSSender = None
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(session,**kwargs)
    async def createClient(self):
        if MessageService.client:
            # logger.info('短信发送客户端已存在，直接返回')
            return MessageService.client
        # logger.info('短信发送客户端不存在，创建客户端') 
        settings = await SysPublicDictionaryDal(self.session).GetDictCacheFirst(config.SystemCode,'short-message',True)
        # settings = await PublicDictionaryDal(self.session).GetDictCacheFirst(config.SystemCode,'short-message')
        channel = settings.get('channel','aliyun')
        access_key = settings.get('access_key')
        access_key_secret = settings.get('access_key_secret')
        if not access_key or not access_key_secret:
            raise Exception('未配置短信发送相关配置')
        if channel == 'aliyun':
            MessageService.client = ALiyunSender(access_key,access_key_secret)
        if not MessageService.client:
            raise Exception('未配置短信发送渠道')
        return MessageService.client
    async def SaveAsJson(self,jsonData):
        dal = MessageSendSettingDal(self.session)
        Id = jsonData.get('Id')
        EventId = jsonData.get('EventId')
        if not EventId:
            raise FriendlyException('请传入事件编号')
        EventName = jsonData.get('EventName')
        PreDay = int(jsonData.get('PreDay'))
        if PreDay<=0:
            raise FriendlyException('提前天数必须大于等于0')
        exist = await dal.GetByEvent(EventId,EventName)
        if exist:
            if exist.UID!= self.user_id:
                raise FriendlyException('您没有权限修改此信息')
            exist.PreDay = PreDay
            if exist.Status == SendStatus.Delete.value:
                exist.Status = SendStatus.Wait.value
                exist.IsDelete = 0
                await SysUserExtendDal(self.session).ReduceCount(self.user_id)
            self.genNextSendTime(exist)
            self.generatParam(exist)
            await dal.Update(exist)
            return exist
        else:
            return await self.AddByJson(jsonData)
    async def CloseSendSetting(self,id):
        dal = MessageSendSettingDal(self.session)
        await dal.CloseSendSetting(id)
        await SysUserExtendDal(self.session).AddCount(self.user_id)
        
    async def AddByJson(self,jsonData):
        EventId = jsonData.get('EventId')
        EventName = jsonData.get('EventName')
        PreDay = jsonData.get('PreDay')
        if not EventId or not EventName or not PreDay:
            return None
        await SysUserExtendDal(self.session).ReduceCount(self.user_id)
        if EventName=='生日':
            return await self.SetBirthdayRemind(jsonData)
        elif EventName=='friend_moment':
            return await self.SetMomentRemind(jsonData)
    async def CloseBirthDayRemind(self,friendId):
        msgSendDal= MessageSendSettingDal(self.session)
        await msgSendDal.CloseBirthDayRemind(self.user_id,friendId)
        await SysUserExtendDal(self.session).AddCount(self.user_id)

    def generatParam(self,setting:MessageSendSetting,**args):
        if setting.EventName == "生日":
            setting.SendTemplateParam = json.dumps({"name":'data.FriendNikeName',"day":int(setting.PreDay)},ensure_ascii=False)
        elif setting.EventName == "纪念日":
            # 还有${day}天，是您和${name}的${title}纪念日，请知悉。
            setting.SendTemplateParam = json.dumps({"name":setting.EventId,"day":int(setting.PreDay)},ensure_ascii=False)
            
    def GenerateMsgSetting(self,setting:MessageSendSetting):
        setting.SendType = "3"
        setting.SendTemplateSign = "快享云上海软件"
        if not setting.SendTemplateCode:
            raise FriendlyException("短信模板编号不能为空")
        self.genNextSendTime(setting)
    def genNextSendTime(self,setting:MessageSendSetting):
        if isinstance(setting.EventDate,str):
            setting.EventDate = datetime.strptime(setting.EventDate,"%Y-%m-%d")
        baseDate:datetime = setting.EventDate
        month = baseDate.month
        day = baseDate.day
        now = date.today()
        
        year = now.year
        Repetetion = int(setting.Repetetion)
        PreDay = int(setting.PreDay)
        EventDateIsLunar = int(setting.EventDateIsLunar)
        # 如果有最后一次发送时间，则从最后一次发送时间开始计算
        if setting.LastSendTime:
            lastTime:datetime = setting.LastSendTime + timedelta(days=PreDay)
            if Repetetion == RepetetionTypes.EveryYear.value:
                year = lastTime.year + 1
            elif Repetetion == RepetetionTypes.EveryMonth.value:
                if month == 12:
                    month = 1
                    year = lastTime.year + 1
                else:
                    month = lastTime.month + 1
            else:
                raise FriendlyException('发送短信不支持的发送周期配置，目前只支持按年、按月')
                    
        nextTime = date(year, month, day)
        if EventDateIsLunar==1:
            d= LunarDate(year, month, day)
            nextTime = d.toSolarDate()
        nextTime = nextTime+timedelta(days=-PreDay)
        
        if nextTime< now:
            setting.LastSendTime = now
            return self.genNextSendTime(setting)
        setting.NextSendTime = nextTime
        return setting
    async def updateNextSendTime(self,setting:MessageSendSetting):
        self.genNextSendTime(setting)
        setting.Status = SendStatus.Wait.value
        await MessageSendSettingDal(self.session).Update(setting)

    async def send_message(self):
        sender =await self.createClient()
        msgSendDal= MessageSendSettingDal(self.session)
        msgRecordDal = MessageSendRecordDal(self.session)
        userDal = SysUsersDal(self.session)
        pageIndex=1
        pageSize=100
        settings =await msgSendDal.GetNeedSendSettings(SendTypes.Sms.value,pageIndex,pageSize)
        tempUser:SysUsers =None
        while settings:
            for setting in settings:
                if not tempUser or tempUser.Id!=setting.UID:
                    tempUser = await userDal.GetUserPhone(setting.UID)
                    if not tempUser:
                        setting.Status = 9
                        setting.Remark = '没有找到用户信息，或者用户未激活'
                        await msgSendDal.Update(setting)
                        continue
                    if not tempUser.PhoneNumber:
                        setting.Status = SendStatus.Fail.value
                        setting.Remark = '用户未配置手机号'
                        await msgSendDal.Update(setting)
                        continue
                try:
                    param = await self.generat_send_param(setting)
                    requestId = await sender.send_message(tempUser.PhoneNumber,setting.SendTemplateSign,setting.SendTemplateCode,param)
                    await msgRecordDal.AddSendRecord(tempUser.PhoneNumber,requestId,setting,1)
                    setting.SendTemplateParam = param
                    if config.ENV_NAME!='dev':
                        setting.LastSendTime = datetime.now()
                        await self.updateNextSendTime(setting)
                except Exception as ex:
                    logger.error(f'发送短信出错:{ex}')
                    await msgRecordDal.AddSendRecord(tempUser.PhoneNumber,'',setting,5,str(ex))
                    setting.Status = SendStatus.Wait.value
                    setting.Remark = str(ex)[0:200]
                    await msgSendDal.Update(setting)
            pageIndex+=1
            if len(settings)<pageSize:
                break
            settings =await msgSendDal.GetNeedSendSettings(SendTypes.Sms.value,pageIndex,pageSize)
        
    async def SendToWeChat(self,msg):
        try:
            url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6cd960da-57fe-4675-80af-43e143964512'
            data = {
                "msgtype": "text",
                "text": {
                    "content": msg
                }
            }
            requests.post(url, json=data)
        except Exception as ex:
            logger.error(ex)

    async def BeginSendsms(self):
        asyncio.create_task(self.send_message)

    async def DeleteFriend(self,friendId:str):
        dal = MessageSendSettingDal(self.session)
        events =await dal.GetByEvents(friendId,'生日')
        userDal = SysUserExtendDal(self.session)
        for event in events:
            await userDal.AddCount(event.UID)
            dal.Delete(event.Id)
    async def SendInteralMsg(self,uid,msgType,title,content):
        await SysUserExtendDal(self.session).AddUnRead(uid)
        await SysMessageDal(self.session).SendMsg(uid,msgType,title,content)
        
    async def UserRegist(self,uid):
        userDal = SysUsersDal(self.session)
        exist = await userDal.GetExist(uid)
        dal = SysUserExtendDal(self.session)
        await dal.InitUser(uid)
        if exist.RegistFrom:
            user =await userDal.Get(exist.RegistFrom)
            # 增加一个免费短信额度
            if user:
                await dal.UpdateCount(user.Id,1)
                await self.SendInteralMsg(user.Id,MsgTypes.Remind.value,'恭喜您，获得1次免费提醒额度',f'您邀请的用户:{exist.ChineseName}注册成功，获得1次免费提醒额度')
    async def Callback(self,jsonData):
        """处理回调"""
        client =await self.createClient()
        datas = await client.callBack(jsonData)
        for data in datas:
            if not data.requestId:
                logger.error(f'回调数据中没有requestId，数据: {json.dumps(data,ensure_ascii=False)}')
                continue
            await MessageSendRecordDal(self.session).UpdateByRequestId(data.requestId,data.send_time,data.success,data.err_msg)
    async def ReadMsgBatch(self,messageIds):
        dal = SysMessageDal(self.session)
        await dal.UpdateBatch(messageIds)
        await SysUserExtendDal(self.session).ReduceUnRead(self.user_id,len(messageIds))