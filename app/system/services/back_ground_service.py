import asyncio
from app.contract.infra.Iconfig_service import IConfigService
from app.database import AsyncSessionLocal
from app.global_var import MsgTypes
from app.infra.services.file_service import load_master_config
from app.system.services.message_service import MessageService
from app.system.services.orgnization_service import OrgnizationService
from kxy.framework.kxy_logger import KxyLogger
from kxy.framework.mapper import Mapper

logger = KxyLogger.getLogger(__name__)
class BackGroundService():
    @staticmethod
    async def init_message_service():
        async with AsyncSessionLocal() as session:
            messageService = MessageService(session,UserId='0',UserName='system')
            await messageService.createClient()
            
    @staticmethod
    async def init_system():
        async with AsyncSessionLocal() as session:
            try:
                await load_master_config(session)
                # 初始化用户系统工具类
                util = await OrgnizationService.initialize_user_system_util(session)
                configSvc = Mapper.getservice_by_contract(IConfigService, session)
                configSvc.watch('sys.usersource.channel',lambda k,v:asyncio.create_task(OrgnizationService.initialize_user_system_util(session,True)))
                configSvc.watch('sys.usersource.channel.appkey',lambda k,v:asyncio.create_task(OrgnizationService.initialize_user_system_util(session,True)))
                configSvc.watch('sys.usersource.channel.appsec',lambda k,v:asyncio.create_task(OrgnizationService.initialize_user_system_util(session,True)))
                asyncio.create_task(util.refresh_token_task())
            except Exception as e:
                logger.error(e)
            # messageService = MessageService(session,UserId='0',UserName='system')
            # await messageService.createClient()
    @staticmethod
    async def send_message_task():
        async with AsyncSessionLocal() as session:
            messageService = MessageService(session,UserId='0',UserName='system')
            await messageService.send_message()
            
    @staticmethod
    async def send_interal_message(uid,title,content):
        async with AsyncSessionLocal() as session:
            messageService = MessageService(session,UserId='0',UserName='system')
            await messageService.SendInteralMsg(uid,MsgTypes.Remind.value,title,content)
            
    @staticmethod
    async def update_birthday_sending_task(uid,friendId):
        async with AsyncSessionLocal() as session:
            messageService = MessageService(session,UserId=uid,UserName=uid)
            await messageService.UpdateBirthdayRemind(uid,friendId)
            
    @staticmethod
    async def update_moment_sending_task(uid,momentId):
        async with AsyncSessionLocal() as session:
            messageService = MessageService(session,UserId=uid,UserName=uid)
            await messageService.UpdateMomentRemind(uid,momentId)
    
    @staticmethod
    async def user_regist(uid):
        async with AsyncSessionLocal() as session:
            messageService = MessageService(session,UserId=uid,UserName=uid)
            await messageService.UserRegist(uid)