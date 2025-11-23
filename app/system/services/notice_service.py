import json
from app.system.dal.system_notify_message_dal import SystemNotifyMessageDal
from app.system.dal.system_notify_template_dal import SystemNotifyTemplateDal
from app.system.models.system_notify_message import SystemNotifyMessage
from app.system.services.base_service import BaseService
from kxy.framework.friendly_exception import FriendlyException
from app.tools import utils


class NoticeService(BaseService):
    async def SendNotifyMessage(self,userid,user_type, templateCode:str,**args):
        '''
        发送通知消息
        @param userid: 用户id
        @param templateCode: 模板编码
        @param args: 参数
        '''
        dal = SystemNotifyMessageDal(self.session)
        tempDal = SystemNotifyTemplateDal(self.session)
        template = await tempDal.GetByCode(templateCode)
        if not template:
            raise FriendlyException('模版不存在')
        msg = SystemNotifyMessage()
        msg.userId= userid
        msg.userType = user_type
        msg.templateType = template.type
        msg.templateId = template.id
        msg.templateCode = template.code
        msg.templateNickname = template.nickname
        msg.templateContent = utils.replace_str_params(template.content,**args)
        msg.templateParams = json.dumps(args,ensure_ascii=False)
        msg.readStatus = 0
        await dal.Insert(msg)
        return msg