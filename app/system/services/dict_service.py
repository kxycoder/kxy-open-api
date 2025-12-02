from app.system.dal.system_dict_data_dal import SystemDictDataDal
from app.system.dal.system_dict_type_dal import SystemDictTypeDal
from app.system.models.system_dict_data import SystemDictData
from app.system.models.system_dict_type import SystemDictType
from app.system.services.base_service import BaseService
from kxy.framework.friendly_exception import FriendlyException
from kxy.framework.delete_safe_list import DeleteSafeList

class DictService(BaseService):
    async def Delete(self,dictId):
        dal = SystemDictTypeDal(self.session)
        exist =await dal.GetExist(dictId)
        
        await dal.Delete(dictId)
        dataDal = SystemDictDataDal(self.session)
        await dataDal.DeleteByType(exist.type)
    async def DeleteBatch(self,keys):
        for key in keys:
            await self.Delete(key)
    async def AddDictDataByJson(self,jsonData):
        typeDal = SystemDictTypeDal(self.session)
        dal = SystemDictDataDal(self.session)
        
        entity=SystemDictData()
        entity.InitInsertEntityWithJson(jsonData)
        exist =await typeDal.GetByType(entity.dictType)
        await dal.Insert(entity)
        return entity
    async def SaveAll(self,jsonData):
        typeDal = SystemDictTypeDal(self.session)
        dal = SystemDictDataDal(self.session)
        dictType = jsonData.get('dictType')
        dictTypeInfo = await typeDal.GetByType(dictType)
        if dictTypeInfo :
            if dictTypeInfo.tenantId != self.tenantId:
                raise FriendlyException("不能操作系统默认字典")
            else:
                dictTypeName = jsonData.get('dictTypeName')
                if dictTypeName:
                    dictTypeInfo.name = jsonData.get('dictTypeName')
                    await typeDal.Update(dictTypeInfo)
        else:
            dictTypeInfo = SystemDictType()
            dictTypeInfo.name=jsonData.get('dictTypeName')
            dictTypeInfo.type = dictType
            dictTypeInfo.status = 0
            await typeDal.Insert(dictTypeInfo)
            
        existDatas = await dal.GetByType(dictType)
        existIds = [exist.id for exist in existDatas]
        values = jsonData.get('list')
        updateIds = []
        for value in values:
            update_id = value.get('id')
            rowDictType = value.get('dictType')
            if update_id and rowDictType==dictType:
                updateIds.append(update_id)
                entity = await dal.Get(update_id)
                entity.InitUpdateFiles(value)
                entity.dictType = dictType
                await dal.Update(entity)
            else:
                if update_id:
                    value.pop('id')
                value['dictType'] = dictType
                entity = SystemDictData()
                entity.InitInsertEntityWithJson(value)
                entity.dictType = dictType
                entity.status = 0
                await dal.Insert(entity)
        
        needDelete,_ = DeleteSafeList(existIds).diffrent_with(updateIds)
        if needDelete:
            await dal.DeleteBatch(needDelete)

        