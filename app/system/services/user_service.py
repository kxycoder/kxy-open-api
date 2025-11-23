
import asyncio
from datetime import datetime, timedelta
import traceback
from typing import List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.auth import IsSuperAdmin
from app.contract.types.user_vo import VoUserRole
from app.common.crypto_util import Crypto
from kxy.framework.friendly_exception import FriendlyException
from app.system.api.types.vo_request import VoSocialAuthRedirect
from app.system.dal.system_dept_dal import SystemDeptDal
from app.system.dal.system_menu_dal import SystemMenuDal
from app.system.dal.system_oauth2_access_token_dal import SystemOauth2AccessTokenDal
from app.system.dal.system_oauth2_refresh_token_dal import SystemOauth2RefreshTokenDal
from app.system.dal.system_post_dal import SystemPostDal
from app.system.dal.system_role_dal import SystemRoleDal
from app.system.dal.system_role_menu_dal import SystemRoleMenuDal
from app.system.dal.system_social_client_dal import SystemSocialClientDal
from app.system.dal.system_social_user_bind_dal import SystemSocialUserBindDal
from app.system.dal.system_social_user_dal import SystemSocialUserDal
from app.system.dal.system_users_dal import SystemUsersDal
from app.global_var import Gkey,Keys
from kxy.framework.mapper import Mapper
from app.system.models.sys_users import SysUsers
from app.system.models.system_oauth2_access_token import SystemOauth2AccessToken
from app.system.models.system_role import SystemRole
from app.system.models.system_users import SystemUsers
from app.system.services.base_service import BaseService
from app.system.dal.sys_users_dal import SysUsersDal
from app.system.dal.system_user_role_dal import SystemUserRoleDal
from app.system.services.social.auth_enums import AuthSource, AuthTypes, DingTalkAuth,DingTalkV2Auth, WeChatQiyeWeixinAuth
from app.system.services.social.auth_token import AuthToken
from app.system.services.social.dingtalk import DingTalk
from app.system.services.social.qiye_weixin import QiyeWeixin
from app.tools.wx_util import WxUtil
from app.tools import utils
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)
from app.config import config
from jose import jwt
from kxy.framework.mapper import Mapper
from app.database import redisClient
from kxy.framework.context import access_token,kxy_roles

# https://docs.wechatpy.org/zh-cn/stable/
class UserService(BaseService):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__(db,**kwargs)


    async def LoginWx(self,code,sourceUser='',sourceId='',sourceType=''):
        dal=SysUsersDal(self.session)
        wxUtil = WxUtil()
        openId =await wxUtil.get_wx_user_openid(code)
        user =await dal.GetUserByOpenId(openId)
        if not user:
            user =await dal.RegistByOpenId(openId, '',sourceUser,sourceId,sourceType)
            if sourceUser:
                bgSvc = Mapper.getservice('BackGroundService')
                asyncio.create_task(bgSvc.user_regist(user.Id))
        else:
            user.LastLoginDate = datetime.now()
            await dal.Update(user)
        result = user.to_mini_dict()
        result['token']=await self.GenerateToken(user)
        return result
    async def UpdateUserPhone(self,code):
        dal=SysUsersDal(self.session)
        userInfo  = await dal.GetCurrentUser()
        if not userInfo:
            raise FriendlyException('用户信息获取失败')
        if not userInfo.PhoneNumber:
            wxUtil = WxUtil()
            userInfo.PhoneNumber = await wxUtil.get_wx_user_phone(code)
            await dal.Update(userInfo)
        return userInfo
    async def GenerateToken(self,user:SysUsers):
        ACCESS_TOKEN_EXPIRE_SECONDES = config.ACCESS_TOKEN_EXPIRE_SECONDES  # 可自定义过期时间
        expire = datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDES)
        roles = await self.GetUserRolesNameCache(user.Id,True)
        payload = {
            "id": user.Id,  # 存储用户ID
            "chineseName":user.ChineseName,
            "departmentId":'',
            "roles":roles,
            "exp": int(expire.timestamp())  # 过期时间
        }
        # 普通用户使用jwt登录
        encoded_jwt = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
        return encoded_jwt
    async def GenerateTenantAccessToken(self, user:SystemUsers,tenantId:int=1)->SystemOauth2AccessToken:
        # 后台用户通过授权登录
        payload = {
            "id": user.id,  # 存储用户ID
            "chineseName":user.nickname,
            "tenantId":tenantId,
            "departmentId":'',
        }
        token =await self.GenerateAccessToken(user,tenantId)
        key = Gkey(Keys.USER_API_TOKEN,token.accessToken)
        await redisClient.set_json(key, payload, config.ACCESS_TOKEN_EXPIRE_SECONDES)
        return token
    async def RefreshToken(self,refreshToken)->str:
        refreshDal = SystemOauth2RefreshTokenDal(self.session)
        refreshTokenInfo = await refreshDal.GetByToken(refreshToken)
        if not refreshTokenInfo:
            raise FriendlyException('无效的刷新令牌')
        if not utils.is_expire(refreshTokenInfo.expiresTime):
            raise FriendlyException('刷新令牌已过期')
        dal = SystemOauth2AccessTokenDal(self.session)
        accessToken = await dal.GetByRefreshToken(refreshTokenInfo.refreshToken)
        if accessToken:
            if not utils.is_expire_after(accessToken.expiresTime,minute=10):
                return accessToken.accessToken

        accessToken = await dal.CreateToken(refreshTokenInfo.userId,refreshTokenInfo.refreshToken,refreshTokenInfo.tenantId)
        return accessToken.accessToken
        
    async def GenerateAccessToken(self, user:SystemUsers,tenantId:int=1)->SystemOauth2AccessToken:
        accessTokenDal = SystemOauth2AccessTokenDal(self.session)
        refreshTokenDal = SystemOauth2RefreshTokenDal(self.session)
        refreshToken = await refreshTokenDal.getUserToken(user.id,tenantId)
        
        if not refreshToken:
            refreshToken = await refreshTokenDal.AddRefreshToken(user,tenantId)
            accessToken = await accessTokenDal.CreateToken(user.id,refreshToken.refreshToken,tenantId)
        else:
            if utils.is_expire_after(refreshToken.expiresTime,minute=10):
                await refreshTokenDal.Clear(user.id,tenantId)
                refreshToken = await refreshTokenDal.AddRefreshToken(user,tenantId)
                accessToken = await accessTokenDal.CreateToken(user.id,refreshToken.refreshToken,tenantId)
            else:
                accessToken = await accessTokenDal.GetByRefreshToken(refreshToken.refreshToken)
                if not accessToken:
                    accessToken = await accessTokenDal.CreateToken(user.id,refreshToken.refreshToken,tenantId)
        return accessToken

    async def Login(self, userName, password):
        dal=SystemUsersDal(self.session)
        password=Crypto().encrypt(password)
        user=await dal.Login(userName,password)
        return await self.LoginWithUserInfo(user)
    async def LoginWithUserInfo(self,user:SystemUsers):
        if user:
            if user.tenantId is None:
                raise FriendlyException('用户未绑定租户')
            # tenantIds =  user.tenantId.split(',')
            tenantId = user.tenantId
            # if len(tenantIds)>1:
            #     # todo johnliu 处理一个账户具有多租户的逻辑
            #     pass
            token =await self.GenerateTenantAccessToken(user,tenantId)
            return {
                "userId": user.id,
                "accessToken": token.accessToken,
                "refreshToken": token.refreshToken,
                "expiresTime": 1754036950266
            }
        else:
            return None

    async def GetUserInfo(self)->SystemUsers:
        dal = SystemUsersDal(self.session)
        return await dal.GetCurrentUser()
    async def RegistUser(self,userName,password,phone):
        dal = SysUsersDal(self.session)
        user = await dal.AddNewUser(userName,password,phone)
        return user
        # familyDal = FriendFamilyDal(self.db)
        # await familyDal.CreateFamily(user.Id)
    async def UpdateUserInfo(self,userInfo):
        # {"Sex":"1","NickName":"路人甲","Avater":"http://tmp/fzC3lYdBbHHP3c9404e269880df7d7370d26e9f89fdf.jpeg","summary":"我是一个好人"}
        dal = SysUsersDal(self.session)
        currentUser = await dal.GetCurrentUser()
        currentUser.Avater = userInfo.get('Avater')
        currentUser.NickName = userInfo.get('NickName')
        # currentUser.EnglishName = jsonData.get('englishName')
        currentUser.Sex = userInfo.get('Sex')
        currentUser.Remark = userInfo.get('Remark')
        await dal.Update(currentUser)
    async def Logout(self):
        token = access_token.get()
        if token:
            await self.DeleleteAccessToken(token)
    async def GetMyPerrmission(self,userid):
        userRoleIds = await self.GetUserRoleIds(userid)
        if not userRoleIds:
            return []
        menuIds =await SystemRoleMenuDal(self.session).GetRolesMenuId(userRoleIds)
        if not menuIds:
            return []
        schemas = await SystemMenuDal(self.session).GetMenuSchemas(menuIds)
        return schemas
    async def CheckSchema(self,userid,schema):
        schemas =await self.GetMyPerrmission(userid)
        return schema in schemas
    async def GetUserRoleIds(self,userid):
        key = Gkey(Keys.USER_ROLES_ID,self.tenantId,userid)
        roles = await redisClient.get_json(key)
        if not roles:
            roles = await SystemUserRoleDal(self.session).GetUserRoleIds(userid)
            await redisClient.set_json(key,roles,ex=86400)
        return roles

    async def GetUserRolesNameCache(self,userid,clearCache=False):
        key = Gkey(Keys.USER_ROLES,self.tenantId,userid)
        roles=[]
        if not clearCache:
            roles = await redisClient.get_json(key)
        if not roles:
            roleIds = await self.GetUserRoleIds(userid)
            roles = await SystemRoleDal(self.session).GetRoleNameByIds(roleIds)
            await redisClient.set_json(key,roles,ex=86400)
        return roles
    async def GetUserRoles(self,userid)->List[SystemRole]:
        roleIds = await self.GetUserRoleIds(userid)
        return await SystemRoleDal(self.session).GetRolesByIds(roleIds)
    
    async def GetUserMenu(self,clearCache=False):
        if IsSuperAdmin():
            return await SystemMenuDal(self.session).GetSimpleList({})
        userRoleIds = await self.GetUserRoleIds(self.user_id)
        menuIds =await SystemRoleMenuDal(self.session).GetRolesMenuId(userRoleIds)
        if not menuIds:
            return []
        menus = await SystemMenuDal(self.session).GetMenuByIds(menuIds)
        return menus
    async def GetUserMenuAndActions(self):
        try:
            userRoleIds = await self.GetUserRoleIds(self.user_id)
            menuIds =await SystemRoleMenuDal(self.session).GetRolesMenuId(userRoleIds)
            if not menuIds:
                return []
            menus = await SystemMenuDal(self.session).GetMenuByIds(menuIds)
            permissions = [menu.permission for menu in menus if menu.permission]
            treeMenus = [menu for menu in menus if menu.type in [1,2]]
            userRoleNames = await self.GetUserRolesNameCache(self.user_id)
            userInfo = await self.GetUserInfo()
            result ={
                'menus': utils.tree(treeMenus),
                'permissions':permissions,
                'roles':userRoleNames,
                'user':userInfo.to_mini_dict()
                }
            return result
        except Exception as ex:
            logger.error(traceback.format_exc(limit=5))
            raise ex
    async def DeleteUser(self,userid):
        dal = SystemUsersDal(self.session)
        await dal.Delete(userid)
        await SystemUserRoleDal(self.session).DeleteByUser(userid)
    async def UpdateUserStatus(self,id,status):
        dal = SystemUsersDal(self.session)
        await dal.UpdateUserStatus(id,status)
    async def AssignUserRole(self,roles:VoUserRole):
        tenantRoles =await SystemRoleDal(self.session).GetAllTenantRoles()
        for role in roles.roleIds:
            if role not in tenantRoles:
                raise FriendlyException(f'角色{role}不存在于当前集团中')
        await SystemUserRoleDal(self.session).AssignUserRole(roles)
    async def DeleleteAccessToken(self,accessToken):
        dal = SystemOauth2AccessTokenDal(self.session)
        await dal.DeleteByAccessToken(accessToken)
        key = Gkey(Keys.USER_API_TOKEN,accessToken)
        await redisClient.delete(key)
    async def GetUserById(self,userId)->SystemUsers:
        dal=SystemUsersDal(self.session)
        return await dal.Get(userId)
    async def GetProfile(self)->dict:
        deptDal = SystemDeptDal(self.session)
        postDal = SystemPostDal(self.session)
        user = await self.GetUserInfo()
        
        user_dict = user.to_basic_dict()
        user_dict['roles'] =await self.GetUserRoles(user.id)
        user_dict['dept'] = await deptDal.GetExist(user.deptId)
        user_dict['posts'] = await postDal.GetByIds(user.postIds)
        
        return user
    async def GetSocialUserBinding(self):
        dal = SystemSocialUserBindDal(self.session)
        users =  await dal.GetBindingUsers(self.user_id)
        socialUsers = await SystemSocialUserDal(self.session).GetByIds([user.socialUserId for user in users])
        socialUserDict = {user.id:user for user in socialUsers}
        for user in users:
            user.openid = socialUserDict.get(user.socialUserId).openid
        return users
    async def BindingSocialUser(self,jsonData)->SystemUsers:
        authType = jsonData.get('type')
        auth = await self.GetAuthType(authType)
        code = jsonData.get('code')
        state = jsonData.get('state')
        token = AuthToken(access_code=code)
        
        userinfo =await auth.get_user_info(auth_token=token)
        userinfo.state = state
        userinfo.code = code
        socialUserInfo = await SystemSocialUserDal(self.session).GetByOpenId(authType,userinfo.unionid)
        if not socialUserInfo:
            socialUserInfo = await SystemSocialUserDal(self.session).AddByField(authType,userinfo)
        bindingDal = SystemSocialUserBindDal(self.session)
        socialUserBindingInfo = await bindingDal.GetBySocial(authType,socialUserInfo.id)
        if socialUserBindingInfo and socialUserBindingInfo.userId!=self.user_id:
            raise FriendlyException('该用户已绑定其他账号，请先解绑')
        await bindingDal.AddBinding(authType,socialUserInfo.id,self.user_id)
    async def UnbindingSocialUser(self,jsonData)->SystemUsers:
        # {"type":20,"openid":"aMxYiSBEeIkSwGrLZqJpQRgiEiE"}
        authType = jsonData.get('type')
        if authType:
            authType = int(authType)
        openid = jsonData.get('openid')
        socialUserInfo = await SystemSocialUserDal(self.session).GetByOpenId(authType,openid)
        if not socialUserInfo:
            raise FriendlyException('该用户不存在')
        dal = SystemSocialUserBindDal(self.session)
        socialUserBindingInfo = await dal.GetBySocial(authType,socialUserInfo.id)
        if socialUserBindingInfo and socialUserBindingInfo.userId==self.user_id:
            await dal.Delete(socialUserBindingInfo.id)
        else:
            raise FriendlyException('该用户不存在')
    async def SocialAuthRedirect(self,type,redirectUri):
        auth = await self.GetAuthType(type,redirectUri)
        return auth.get_auth_url(state=uuid.uuid4().hex)
    async def GetAuthType(self,authType,redirectUri=''):
        authType = int(authType)
        dal = SystemSocialClientDal(self.session)
        auType = AuthTypes(authType)
        config = await dal.GetBySocialType(authType)
        config.redirectUri = redirectUri
        if auType == AuthTypes.DINGTALK:
            source = DingTalkAuth()
            return DingTalk(source=source,config=config)
        elif auType == AuthTypes.WECHAT:
            source = WeChatQiyeWeixinAuth()
            return QiyeWeixin(source=source,config=config)
        else:
            raise FriendlyException(f'暂不支持该第三方登录, {authType}')
        
    async def SocialLogin(self,data:VoSocialAuthRedirect):
        authType = await self.GetAuthType(data.type)
        code = data.code
        state = data.state
        token = AuthToken(access_code=code)
        userinfo =await authType.get_user_info(auth_token=token)
        userinfo.state = state
        userinfo.code = code
        socialUserInfo = await SystemSocialUserDal(self.session).GetByOpenId(data.type,userinfo.unionid)
        if not socialUserInfo:
            raise FriendlyException('该用户不存在')
        bindingDal = SystemSocialUserBindDal(self.session)
        socialUserBindingInfo = await bindingDal.GetBySocial(data.type,socialUserInfo.id)
        if socialUserBindingInfo:
            user = await self.GetUserById(socialUserBindingInfo.userId)
            return await self.LoginWithUserInfo(user)
        raise FriendlyException('该用户未绑定账号')