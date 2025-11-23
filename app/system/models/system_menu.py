from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger,Boolean

class SystemMenu(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'system_menu'

    id = Column('id',Integer, comment='菜单ID',primary_key=True,autoincrement=True)
    name = Column('name',String(50), comment='菜单名称')
    permission = Column('permission',String(100), comment='权限标识')
    type = Column('type',Integer, comment='菜单类型')
    sort = Column('sort',Integer, comment='显示顺序')
    parentId = Column('parent_id',Integer, comment='父菜单ID')
    path = Column('path',String(200), comment='路由地址')
    icon = Column('icon',String(100), comment='菜单图标')
    component = Column('component',String(255), comment='组件路径')
    componentName = Column('component_name',String(255), comment='组件名')
    status = Column('status',Integer, comment='菜单状态')
    visible = Column('visible',Boolean, comment='是否可见',default=True)
    keepAlive = Column('keep_alive',Boolean, comment='是否缓存')
    alwaysShow = Column('always_show',Boolean, comment='是否总是显示')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除')


    InsertRequireFields = []

    InsertOtherFields= ['name', 'permission', 'path', 'icon', 'component', 'componentName','type', 'sort', 'parentId', 'status', 'visible', 'keepAlive', 'alwaysShow']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'permission': self.permission,
           'type': self.type,
           'sort': self.sort,
           'parentId': self.parentId,
           'path': self.path,
           'icon': self.icon,
           'component': self.component,
           'componentName': self.componentName,
           'status': self.status,
           'visible': self.visible,
           'keepAlive': self.keepAlive,
           'alwaysShow': self.alwaysShow,
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
           'name': self.name,
           'permission': self.permission,
           'type': self.type,
           'sort': self.sort,
           'parentId': self.parentId,
           'path': self.path,
           'icon': self.icon,
           'component': self.component,
           'componentName': self.componentName,
           'visible': self.visible,
           'keepAlive': self.keepAlive,
           'alwaysShow': self.alwaysShow,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [SystemMenu.id,SystemMenu.name,SystemMenu.permission,SystemMenu.type,SystemMenu.sort,SystemMenu.parentId,SystemMenu.path,SystemMenu.icon,SystemMenu.component,SystemMenu.componentName,SystemMenu.visible,SystemMenu.keepAlive,SystemMenu.alwaysShow,SystemMenu.status]