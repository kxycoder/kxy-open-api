# coding=UTF-8

from app.common.basedal import BaseDal
from kxy.framework.friendly_exception import FriendlyException
from sqlalchemy.ext.asyncio import AsyncSession
from app.system.models.sys_public_dictionary import PublicDictionary
from sqlalchemy import and_,or_
import re,json
# from exts import getRedis
from app.database import get_redis_client
from typing import List as ListType
from app.global_var import Gkey,Keys
class SysPublicDictionaryDal(BaseDal[PublicDictionary]):
    def __init__(self,db:AsyncSession,**kwargs):
        super().__init__(PublicDictionary,db,**kwargs)
        self.CacheKey = 'optsso:dictionary:'
        self.cache=get_redis_client()

    async def GetCacheKey(self,systemcode, dictype):
        return Gkey(Keys.PUBLIC_DICTIONARY_CACHE_KEY,systemcode,dictype)
        # return self.CacheKey+'%s:%s'%(systemcode,dictype)
    async def GetIntCacheKey(self,systemcode, dictype):
        return Gkey(Keys.PUBLIC_DICTIONARY_CACHE_TYPE_KEY,systemcode,dictype,'int')
        # return self.CacheKey+'%s:%s:int'%(systemcode,dictype)

    async def GetCacheKeyDict(self, systemcode,dictype):
        return Gkey(Keys.PUBLIC_DICTIONARY_CACHE_TYPE_KEY,systemcode,dictype,'dict')
        # return self.CacheKey+'%s:%s:d'%(systemcode,dictype)
    async def GetIntCacheKeyDictKey(self, systemcode,dictype):
        return Gkey(Keys.PUBLIC_DICTIONARY_CACHE_TYPE_KEY,systemcode,dictype,'dictInt')
        
        # return self.CacheKey+'%s:%s:d:int'%(systemcode,dictype)
    
    # 获取列表
    async def List(self,search,page_index, page_size):
        fil = list()
        # fil.append(PublicDictionary.Status != 10)
        if search.get('search'):
           if re.search(r"^(\d)*$", search):
               fil.append(PublicDictionary.Id == int(search))
           else:
               search =search.strip()
               fil.append(or_(PublicDictionary.DicType.ilike("%" + search + "%"),
                              PublicDictionary.Key.ilike("%" + search + "%"),
                              PublicDictionary.Title.ilike("%" + search + "%"),
                              PublicDictionary.Description.ilike("%" + search + "%")))
        if search.get('systemcode'):
            fil.append(PublicDictionary.SystemCode==search.get('systemcode'))
        dictType = search.get('dicType')
        if dictType:
            fil.append(PublicDictionary.DicType == dictType)
        total,datas = await self.paginate_query(fil,PublicDictionary.DicType.asc(),page_index,page_size)
        # f=self.session.query(PublicDictionary).filter(*fil)
        # total=f.count()
        # datas=f.order_by(PublicDictionary.CreateDate.desc()).offset((page_index-1)*page_size).limit(page_size)
        return total,datas
    # 创建

    async def AddByJsonData(self, jsonData):
        entity = PublicDictionary()
        entity.InitInsertEntityWithJson(jsonData)
        entity.Status = 5
        await self.Insert(entity)
        await self.ClearCache(entity.SystemCode,entity.DicType)
        return entity

    async def Delete(self, id):
        exist = await self.Get(id)
        if exist != None:
            exist.Status = 10
            await self.Update(exist)
            await self.ClearCache(exist.SystemCode,exist.DicType)
        else:
            raise FriendlyException('不存在'+str(id)+'的数据')

    async def UpdateByJsonData(self, jsonData):
        id = jsonData.get('Id', None)
        if id == None:
            raise FriendlyException('更新时必须传回主键')
        entity = await self.Get(id)
        if not entity:
            raise FriendlyException('不存在'+str(id)+"的数据")
        entity.InitUpdateFiles(jsonData)
        await self.Update(entity)
        await self.ClearCache(entity.SystemCode,entity.DicType)
        return entity

    async def ClearCache(self,systemcode, dictype):
        key = await self.GetCacheKey(systemcode,dictype)
        await self.cache.delete(key)
        dicKey=await self.GetCacheKeyDict(systemcode,dictype)
        await self.cache.delete(dicKey)
        key = await self.GetIntCacheKey(systemcode,dictype)
        await self.cache.delete(key)
        key = await self.GetIntCacheKeyDictKey(systemcode,dictype)
        await self.cache.delete(key)

    async def GetListCacheFirst(self,systemcode, DicType):
        '''
        返回[]
        '''
        key = await self.GetCacheKey(systemcode,DicType)
        items = await self.cache.get(key)
        if items != None:
            return json.loads(items)
        results = await self.GetDictionary(systemcode,DicType)
        items = [item.getKeyValue() for item in results]
        await self.cache.set(key, json.dumps(items),2280)
        return items

    async def GetListIntCacheFirst(self, systemcode,DicType):
        key = await self.GetIntCacheKey(systemcode,DicType)
        items = await self.cache.get(key)
        if items != None:
            return json.loads(items)
        results = await self.GetDictionary(systemcode,DicType)
        items = [item.getIdValue() for item in results]
        await self.cache.set(key, json.dumps(items),2280)
        return items

    async def GetDictCacheFirst(self,systemcode, DicType,refreshCache=False):
        '''
        返回{key:value,key2:value2}
        '''
        key = await self.GetCacheKeyDict(systemcode,DicType)
        if not refreshCache:
            items =await self.cache.get(key)
            if items != None:
                return json.loads(items)
        results = await self.GetDictionary(systemcode,DicType)
        items = {}
        for item in results:
            items[item.Key] = item.Value
        await self.cache.set(key, json.dumps(items),2280)
        return items

    async def GetDictCacheIntFirst(self,systemcode, DicType):
        '''
        返回{}
        '''
        key = await self.GetCacheKeyDict(systemcode,DicType)
        items = await self.cache.get(key)
        if items != None:
            return json.loads(items)
        results = await self.GetDictionary(systemcode,DicType)
        items = {}
        for item in results:
            items[int(item.Key)] = item.Value
        await self.cache.set(key, json.dumps(items),2280)
        return items

    async def GetDictionary(self,systemcode, DicType):
        return await self.QueryWhere([PublicDictionary.DicType == DicType, PublicDictionary.Status == 5, PublicDictionary.SystemCode ==systemcode],orderBy= PublicDictionary.Sort.asc())
    async def GetKeyValue(self,systemcode, dickType, key):
        fil = [PublicDictionary.DicType == dickType, PublicDictionary.Key == key, PublicDictionary.Status == 5, PublicDictionary.SystemCode ==systemcode]
        results = await self.QueryOne(fil,[PublicDictionary.Value])
        if results:
            return results.Value
        else:
            return ''

    async def GetDic(self,systemcode,dictype,key):
        fil = list()
        fil.append(PublicDictionary.SystemCode==systemcode)
        fil.append(PublicDictionary.DicType==dictype)
        fil.append(PublicDictionary.Key==key)
        fil.append(PublicDictionary.Status==5)
        return await self.QueryOne(fil)
    
    async def GetKeys(self,systemcode,dictypes:ListType[str],keys:ListType[str])->ListType[PublicDictionary]:
        fil = list()
        fil.append(PublicDictionary.SystemCode==systemcode)
        fil.append(PublicDictionary.DicType.in_(dictypes))
        fil.append(PublicDictionary.Key.in_(keys))
        fil.append(PublicDictionary.Status==5)
        return await self.QueryWhere(fil,orderBy=PublicDictionary.Sort.asc())
    
    async def GetLastUpdateMenu(self,systemcode,lastTime,endTime):
        fil = list()
        fil.append(PublicDictionary.SystemCode==systemcode)
        fil.append(PublicDictionary.DicType!='RemoteSSOUrl')
        fil.append(or_(and_(PublicDictionary.LastModifiedDate>=lastTime,PublicDictionary.LastModifiedDate<endTime),and_(PublicDictionary.LastModifiedDate==None,PublicDictionary.CreateDate>=lastTime)))
        return await self.QueryWhere(fil)

    async def SyncJsonData(self,jsonData):
        
        exist=await self.GetDic(jsonData['Id'],jsonData['DicType'],jsonData['Key'])
        if exist:
            exist.Value=jsonData['Value']
            exist.Status=jsonData['Status']
            await self.Update(exist)
        else:
            exist = await self.Get(exist.Id)
            if exist==None:
                exist = PublicDictionary()
                exist.InitInsertEntityWithJson(jsonData)
                await self.Insert(exist)
            
    
    async def GetCanEditDictionary(self, systemcode: str, dict_types: ListType[str]) -> list[PublicDictionary]:
        """
        获取指定systemcode下、指定类型（dict_types）且可编辑的public_dictionary字典（Status=5，未删除）
        :param systemcode: 系统编码
        :param dict_types: 字典类型列表
        :return: 字典信息列表（dict）
        """
        from app.system.models.sys_public_dictionary import PublicDictionary
        fil = [
            PublicDictionary.SystemCode == systemcode,
            PublicDictionary.DicType.in_(dict_types),
            PublicDictionary.Status == 5
        ]
        result = await self.QueryWhere(fil, orderBy=PublicDictionary.Sort.asc())
        return result