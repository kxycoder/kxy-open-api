from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String

class SystemDictData(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_dict_data'

    id = Column('id',Integer, comment='字典编码',primary_key=True,autoincrement=True)
    sort = Column('sort',Integer, comment='字典排序')
    label = Column('label',String(100), comment='字典标签')
    value = Column('value',String(100), comment='字典键值')
    dictType = Column('dict_type',String(100), comment='字典类型')
    status = Column('status',Integer, comment='状态（0正常 1停用）')
    colorType = Column('color_type',String(100), comment='颜色类型')
    cssClass = Column('css_class',String(100), comment='css 样式')
    remark = Column('remark',String(500), comment='备注')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)

    InsertRequireFields = ['dictType','label', 'value']

    InsertOtherFields= [ 'colorType', 'cssClass', 'remark','sort', 'status']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'sort': self.sort,
           'label': self.label,
           'value': self.value,
           'dictType': self.dictType,
           'status': self.status,
           'colorType': self.colorType,
           'cssClass': self.cssClass,
           'remark': self.remark,
           'creator': self.creator,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updater': self.updater,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'deleted': self.deleted,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'sort': self.sort,
           'label': self.label,
           'value': self.value,
           'dictType': self.dictType,
           'colorType': self.colorType,
           'cssClass': self.cssClass,
           'remark': self.remark,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemDictData.id,SystemDictData.sort,SystemDictData.label,SystemDictData.value,SystemDictData.dictType,SystemDictData.colorType,SystemDictData.cssClass,SystemDictData.remark]