import csv
import re
from typing import Dict,List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, select, or_
from kxy.framework.friendly_exception import FriendlyException
from app.system.models.system_area import SystemArea
from app.tools import utils

from app.common.basedal import MyBaseDal

class SystemAreaDal(MyBaseDal[SystemArea]):
    def __init__(self,session:AsyncSession,**kwargs):
        super().__init__(SystemArea,session,**kwargs)
    
    # 获取列表
    async def Search(self,search:Dict[str,object],page_index, page_size)->tuple[List[SystemArea],int]:
        fil = list()
        fil.append(SystemArea.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemArea,k) and v:
                fil.append(getattr(SystemArea,k).ilike(f'%{v}%'))
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemArea.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemArea.Name.ilike("%" + search_text + "%"))
            #    fil.append(or_(SystemArea.DicType.ilike("%" + search_text + "%"),
            #                  SystemArea.Description.ilike("%" + search_text + "%")))
        status = search.get('status')
        if status:
            fil.append(SystemArea.status == int(status))
        items, total_count = await self.paginate_query(fil, SystemArea.createTime.desc(), page_index, page_size)
        return items, total_count
    async def SearchByUser(self,search:Dict[str,object],page_index:int, page_size:int, need_count=True)->tuple[List[SystemArea],int]:
        fil = list()
        fil.append(SystemArea.UID == self.UserId)
        fil.append(SystemArea.deleted == 0)
        search_text=search.get('search')
        if search_text:
            if re.search(r"^(\d)*$", search_text):
                fil.append(SystemArea.id == int(search_text))
            #else:
            #    search_text =search_text.strip()
            #    fil.append(SystemArea.Name.ilike("%" + search_text + "%"))
        status = search.get('status')
        if status:
            fil.append(SystemArea.status == int(status))
        total_count = 0
        if need_count:
            total_count = await self.QueryCount(fil)
        items = await self.page_nocount_query(fil, SystemArea.createTime.desc(), page_index, page_size)
        return items, total_count

    async def GetSimpleList(self,search:Dict[str,object],page_index, page_size)->List[SystemArea]:
        fil = list()
        fil.append( SystemArea.deleted == 0)
        for k,v in search.items():
            if hasattr(SystemArea,k) and v:
                fil.append(getattr(SystemArea,k).ilike(f'%{v}%'))
        #search_text=search.get('search')
        #if search_text:
        #    if re.search(r"^(\d)*$", search_text):
        #        fil.append( SystemArea.id == int(search_text))

        #status = search.get('status')
        #if status:
        #    fil.append( SystemArea.status == int(status))
        items = await self.page_fields_nocount_query( SystemArea.get_mini_fields(), fil,  SystemArea.createTime.desc(), page_index, page_size)
        return items
    async def GetSimpleListAll(self,)->List[SystemArea]:
        return await self.QueryWhere([SystemArea.deleted==0],fields=SystemArea.get_mini_fields())

    async def AddByJsonData(self, jsonData)->SystemArea:
        entity = SystemArea()
        entity.InitInsertEntityWithJson(jsonData)    
        entity.status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def AddByJsonDataUser(self, jsonData)->SystemArea:
        entity = SystemArea()
        entity.InitInsertEntityWithJson(jsonData)
        entity.UID=self.UserId
        entity.status = 1
        entity.deleted = 0
        await self.Insert(entity)
        return entity

    async def UpdateByJsonData(self,jsonData)->SystemArea:
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemArea=await self.GetExist(id)
        entity.InitUpdateFiles(jsonData) 
        await self.Update(entity)
        return entity

    async def UpdateByJsonDataUser(self,jsonData)->SystemArea:
        '''更新客户自己的数据'''
        id=jsonData.get('id',None)
        if id==None:
            raise FriendlyException('更新时必须传回主键')
        entity:SystemArea=await self.GetExistByUser(id)
        entity.InitUpdateFiles(jsonData) 
        entity.UID = self.UserId
        await self.Update(entity)
        return entity

    async def Delete(self,id):
        await self.DeleteWhere([SystemArea.id==id])

    async def DeleteByUser(self,id):
        await self.DeleteWhere([SystemArea.id==id,SystemArea.UID==self.UserId])

    async def DeleteBatch(self,ids):
        return await self.DeleteWhere([SystemArea.id.in_(ids)])

    async def DeleteBatchByUser(self,ids):
        return await self.DeleteWhere([SystemArea.id.in_(ids),SystemArea.UID==self.UserId])
    async def init(self):
        import os
        # 获取项目根目录
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # 构造正确的csv文件路径
        csv_path = os.path.join(project_root, 'docs', 'area.csv')
        if not os.path.exists(csv_path):
            raise FriendlyException(f'地区数据文件不存在: {csv_path}')
        
        # 读取已存在的地区数据，避免重复插入
        existing_areas = await self.GetSimpleListAll()
        existing_ids = {area.id for area in existing_areas}
        
        areas_to_insert = []
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                area_id = int(row['id'])
                # 如果地区已存在，跳过
                if area_id in existing_ids:
                    continue
                    
                area_data = {
                    'id': area_id,
                    'name': row['name'],
                    'type': int(row['type']),
                    'parentId': int(row['parentId'])
                }
                
                areas_to_insert.append(area_data)
        # 批量插入新地区数据
        entitys = []
        for area_data in areas_to_insert:
            entity = SystemArea()
            entity.id = area_data['id']
            entity.name = area_data['name']
            entity.type = area_data['type']
            entity.parentId = area_data['parentId']
            entity.status = 0
            entity.deleted = 0
            entitys.append(entity)
        
        await self.BatchInsert(entitys)
        return len(entitys)