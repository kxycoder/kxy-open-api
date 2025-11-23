from app.system.services.base_service import BaseService
from app.system.dal.sys_public_dictionary_type_dal import SysPublicDictionaryTypeDal
from app.system.dal.sys_public_dictionary_dal import SysPublicDictionaryDal


class SettingService(BaseService):
    async def get_user_editable_public_dictionary_types(self,systemcode: str = None):
        """
        获取当前用户可编辑的public_dictionary字典类型（CanEdit=1，未删除，激活状态）
        """
        dal = SysPublicDictionaryTypeDal(self.session, UserId=self.user_id)
        result = await dal.get_user_editable_types(systemcode)
        dictTypes = {item.DicType:item for item in result}
        settings = await SysPublicDictionaryDal(self.session).GetCanEditDictionary(systemcode, list(dictTypes.keys()))
        for setting in settings:
            dictType = dictTypes[setting.DicType]
            dictType.Settings.append(setting)
        return dictTypes