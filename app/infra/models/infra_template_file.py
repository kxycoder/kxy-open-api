from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger,Text
from kxy.framework.base_entity import JSONString

class InfraTemplateFile(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
    __tablename__ = 'infra_template_file'

    id = Column('id',Integer, comment='编号',primary_key=True,autoincrement=True)
    templateId = Column('template_id',Integer, comment='模版编号',autoincrement=True)
    fileType = Column('file_type',String(20), comment='文件类型（main-主文件 child子表文件）',default='main')
    fileModel = Column('file_model',String(5), comment='文件模式（a+追加，w覆盖）',default='w')
    name = Column('name',String(30), comment='文件名称')
    excuteCondtion = Column('excute_condtion',JSONString, comment='执行条件')
    excuteCondtionScript = Column('excute_conditon_script',Text, comment='执行条件脚本')
    filePath = Column('file_path',String(200), comment='文件保存路径')
    content = Column('content',Text, comment='文件内容',default='')
    scriptContent = Column('script_content',Text, comment='脚本文件',default='')
    creator = Column('creator',String(64), comment='创建者')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updater = Column('updater',String(64), comment='更新者')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)


    InsertRequireFields = ['templateId']

    InsertOtherFields= ['name', 'filePath', 'scriptContent','content','excuteCondtion','excuteCondtionScript','fileType','fileModel']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'templateId': self.templateId,
           'fileType':self.fileType,
           'fileModel':self.fileModel,
           'name': self.name,
           'filePath': self.filePath,
           'scriptContent': self.scriptContent,
           'content': self.content,
           'excuteCondtion':self.excuteCondtion,
           'excuteCondtionScript':self.excuteCondtionScript,
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
           'templateId': self.templateId,
           'fileType':self.fileType,
           'fileModel':self.fileModel,
           'name': self.name,
           'excuteCondtion':self.excuteCondtion,
           'excuteCondtionScript':self.excuteCondtionScript,
           'filePath': self.filePath,
           'scriptContent': self.scriptContent,
           'content': self.content,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [InfraTemplateFile.id,InfraTemplateFile.templateId,InfraTemplateFile.fileType,InfraTemplateFile.fileModel,InfraTemplateFile.name,InfraTemplateFile.scriptContent,InfraTemplateFile.excuteCondtionScript,InfraTemplateFile.filePath,InfraTemplateFile.content,InfraTemplateFile.excuteCondtion]