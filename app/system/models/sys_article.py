from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String,BigInteger

class SysArticle(BaseEntity, Base):
    __tablename__ = 'sys_article'

    Id = Column(String(36), comment='Id',primary_key=True)
    Thumb = Column(String(255), comment='Thumb')
    Title = Column(String(255), comment='标题')
    Content = Column(String(0), comment='内容')
    CategoryId = Column(String(36), comment='分类')
    SortOrder = Column(Integer, comment='排序')
    Author = Column(String(32), comment='作者')
    Link = Column(String(255), comment='链接')
    ReadTime = Column(Integer, comment='ReadTime')
    Status = Column(Integer, comment='状态(1-创建 10-删除)')
    IsDelete = Column(Integer, comment='删除')
    CreateUser = Column(String(20), comment='创建用户')
    CreateDate = Column(DateTime, comment='创建时间')
    LastModifiedUser = Column(String(20), comment='最后修改用户')
    LastModifiedDate = Column(DateTime, comment='最后修改时间')

    InsertRequireFields = ['Title', 'CategoryId', 'SortOrder', 'Author', 'Link', 'ReadTime']

    InsertOtherFields= ['Thumb', 'Content', 'Status', 'IsDelete']

    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'Id': self.Id,
           'Thumb': self.Thumb,
           'Title': self.Title,
           'Content': self.Content,
           'CategoryId': self.CategoryId,
           'SortOrder': self.SortOrder,
           'Author': self.Author,
           'Link': self.Link,
           'ReadTime': self.ReadTime,
           'Status': self.Status,
           'IsDelete': self.IsDelete,
           'CreateUser': self.CreateUser,
           'CreateDate': self.CreateDate.strftime("%Y-%m-%d %H:%M:%S") if self.CreateDate else None,
           'LastModifiedUser': self.LastModifiedUser,
           'LastModifiedDate': self.LastModifiedDate.strftime("%Y-%m-%d %H:%M:%S") if self.LastModifiedDate else None,

        }
        return resp_dict