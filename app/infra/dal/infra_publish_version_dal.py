from datetime import datetime
import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.infra.models.infra_publish_version import InfraPublishVersion
from app.tools import utils


from app.common.basedal import MyBaseDal


class InfraPublishVersionDal(MyBaseDal[InfraPublishVersion]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(InfraPublishVersion,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[InfraPublishVersion],int]:
        fil = list()
        fil.append(InfraPublishVersion.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraPublishVersion,k) and v:
                fil.append(getattr(InfraPublishVersion,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(InfraPublishVersion.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(InfraPublishVersion.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(InfraPublishVersion.DicType.ilike("%" + search_text + "%"),
            #                  InfraPublishVersion.Description.ilike("%" + search_text + "%")))

        status = search.get('status')
        if status:
            fil.append(InfraPublishVersion.status == int(status))

        items, total_count = await self.paginate_query(fil, InfraPublishVersion.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[InfraPublishVersion]:
        fil = list()
        fil.append( InfraPublishVersion.deleted == 0)
        for k,v in search.items():
            if hasattr(InfraPublishVersion,k) and v:
                fil.append(getattr(InfraPublishVersion,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( InfraPublishVersion.id == int(search_text))


        #status = search.get('status')
        #if status:
        #    fil.append( InfraPublishVersion.status == int(status))
        items = await self.page_fields_nocount_query( InfraPublishVersion.get_mini_fields(), fil,  InfraPublishVersion.createTime.desc(), page_index, page_size)
        return items

    async def AddByJsonData(self, jsonData)->InfraPublishVersion:
        entity = InfraPublishVersion()
        entity.InitInsertEntityWithJson(jsonData)
        entity.status = 0
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->InfraPublishVersion:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:InfraPublishVersion=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([InfraPublishVersion.id==id])


    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([InfraPublishVersion.id.in_(ids)])
 
    def GeneratVersion(self,version:InfraPublishVersion):
        if version.versionType=='date':
            now = datetime.now()
            version.version1 = now.year
            version.version2 = now.month
            version.version3 = now.day
            if version.version4:
                version.version4 += 1
            else:
                version.version4 = 1
        else:
            if version.version4 is None:
                version.version1 = 1
                version.version2 = 0
                version.version3 = 0
                version.version4 = 0
            version.version4 +=1
            if version.version4 > 15:
                version.version4 = 0
                version.version3 +=1
                if version.version3 > 15:
                    version.version3 = 0
                    version.version2 +=1
                    if version.version2 > 15:
                        version.version2 = 0
                        version.version1 +=1
        preVersion = version.version
        version.preVersion = preVersion
        version.version = str(version.version1) + '.' + str(version.version2) + '.' + str(version.version3) + '.' + str(version.version4)
    async def GetVersionByAppName(self,appName,versionType):
        exist = await self.session.execute(select(InfraPublishVersion).where(InfraPublishVersion.appName==appName,InfraPublishVersion.deleted==0).limit(1))
        exist = exist.scalar()
        if not exist:
            version = InfraPublishVersion()
            version.appName = appName
            version.versionType = versionType
            version.status = 1
            version.deleted = 0
            self.GeneratVersion(version)
            await self.Insert(version)
            return version
        else:
            self.GeneratVersion(exist)
            await self.Update(exist)
            return exist