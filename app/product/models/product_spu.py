from app.database import Base
from app.common.base_entity import BaseEntity
from sqlalchemy import Column, DateTime, Integer, String, BigInteger
from kxy.framework.filter_tenant import FilterTenant
from kxy.framework.base_entity import JSONString

@FilterTenant()
class ProductSpu(BaseEntity, Base):
    def __init__(self):
        super().__init__(id_type='int',auto_id=False)
        
    __tablename__ = 'product_spu'

    id = Column('id',Integer, comment='商品 SPU 编号，自增',primary_key=True,autoincrement=True)
    name = Column('name',String(128), comment='商品名称')
    keyword = Column('keyword',String(256), comment='关键字')
    introduction = Column('introduction',String(256), comment='商品简介')
    description = Column('description',String(0), comment='商品详情')
    categoryId = Column('category_id',Integer, comment='商品分类编号')
    brandId = Column('brand_id',Integer, comment='商品品牌编号')
    picUrl = Column('pic_url',String(256), comment='商品封面图')
    sliderPicUrls = Column('slider_pic_urls',JSONString(2000), comment='商品轮播图地址\n 数组，以逗号分隔\n 最多上传15张')
    sort = Column('sort',Integer, comment='排序字段')
    status = Column('status',Integer, comment='商品状态: 1 上架（开启） 0 下架（禁用） -1 回收')
    specType = Column('spec_type',Integer, comment='规格类型：0 单规格 1 多规格')
    price = Column('price',Integer, comment='商品价格，单位使用：分')
    marketPrice = Column('market_price',Integer, comment='市场价，单位使用：分')
    costPrice = Column('cost_price',Integer, comment='成本价，单位： 分')
    stock = Column('stock',Integer, comment='库存')
    deliveryTypes = Column('delivery_types',JSONString(32), comment='配送方式数组')
    deliveryTemplateId = Column('delivery_template_id',Integer, comment='物流配置模板编号')
    giveIntegral = Column('give_integral',Integer, comment='赠送积分')
    subCommissionType = Column('sub_commission_type',Integer, comment='分销类型')
    salesCount = Column('sales_count',Integer, comment='商品销量')
    virtualSalesCount = Column('virtual_sales_count',Integer, comment='虚拟销量')
    browseCount = Column('browse_count',Integer, comment='商品点击量')
    createTime = Column('create_time',DateTime, comment='创建时间')
    updateTime = Column('update_time',DateTime, comment='更新时间')
    creator = Column('creator',String(64), comment='创建人')
    updater = Column('updater',String(64), comment='更新人')
    deleted = Column('deleted',Integer, comment='是否删除',default=0)
    tenantId = Column('tenant_id',Integer, comment='租户编号')
    skus=[]


    InsertRequireFields = ['categoryId', 'sort', 'status', 'price', 'costPrice', 'stock', 'giveIntegral']
    InsertOtherFields= ['name', 'keyword', 'introduction', 'description', 'brandId', 'picUrl', 'sliderPicUrls', 'specType', 'marketPrice', 'deliveryTypes', 'deliveryTemplateId', 'subCommissionType', 'salesCount', 'virtualSalesCount', 'browseCount']


    def to_basic_dict(self):
        """返回基本信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'keyword': self.keyword,
           'introduction': self.introduction,
           'description': self.description,
           'categoryId': self.categoryId,
           'brandId': self.brandId,
           'picUrl': self.picUrl,
           'sliderPicUrls': self.sliderPicUrls,
           'sort': self.sort,
           'status': self.status,
           'specType': self.specType,
           'price': self.price,
           'marketPrice': self.marketPrice,
           'costPrice': self.costPrice,
           'stock': self.stock,
           'deliveryTypes': self.deliveryTypes,
           'deliveryTemplateId': self.deliveryTemplateId,
           'giveIntegral': self.giveIntegral,
           'subCommissionType': self.subCommissionType,
           'salesCount': self.salesCount,
           'virtualSalesCount': self.virtualSalesCount,
           'browseCount': self.browseCount,
           'createTime': self.createTime.strftime("%Y-%m-%d %H:%M:%S") if self.createTime else None,
           'updateTime': self.updateTime.strftime("%Y-%m-%d %H:%M:%S") if self.updateTime else None,
           'creator': self.creator,
           'updater': self.updater,
           'deleted': self.deleted,
           'tenantId': self.tenantId,

        }
        return resp_dict
    def to_mini_dict(self):
        """返回精简信息"""
        resp_dict = {
           'id': self.id,
           'name': self.name,
           'keyword': self.keyword,
           'introduction': self.introduction,
           'description': self.description,
           'categoryId': self.categoryId,
           'brandId': self.brandId,
           'picUrl': self.picUrl,
           'sliderPicUrls': self.sliderPicUrls,
           'sort': self.sort,
           'specType': self.specType,
           'price': self.price,
           'marketPrice': self.marketPrice,
           'costPrice': self.costPrice,
           'stock': self.stock,
           'deliveryTypes': self.deliveryTypes,
           'deliveryTemplateId': self.deliveryTemplateId,
           'giveIntegral': self.giveIntegral,
           'subCommissionType': self.subCommissionType,
           'salesCount': self.salesCount,
           'virtualSalesCount': self.virtualSalesCount,
           'browseCount': self.browseCount,

        }
        return resp_dict
    @staticmethod
    def get_mini_fields():
        """返回精简信息字段"""
        return [ProductSpu.id,ProductSpu.name,ProductSpu.keyword,ProductSpu.introduction,ProductSpu.description,ProductSpu.categoryId,ProductSpu.brandId,ProductSpu.picUrl,ProductSpu.sliderPicUrls,ProductSpu.sort,ProductSpu.specType,ProductSpu.price,ProductSpu.marketPrice,ProductSpu.costPrice,ProductSpu.stock,ProductSpu.deliveryTypes,ProductSpu.deliveryTemplateId,ProductSpu.giveIntegral,ProductSpu.subCommissionType,ProductSpu.salesCount,ProductSpu.virtualSalesCount,ProductSpu.browseCount]