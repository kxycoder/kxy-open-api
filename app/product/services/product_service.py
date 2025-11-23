from typing import List
from kxy.framework.base_service import BaseService
from app.product.dal.product_comment_dal import ProductCommentDal
from app.product.dal.product_sku_dal import ProductSkuDal
from app.product.dal.product_spu_dal import ProductSpuDal
from app.product.models.product_comment import ProductComment
from app.product.models.product_spu import ProductSpu

class ProductService(BaseService):
    async def GetSpuDetail(self,id)->ProductSpu:
        dal = ProductSpuDal(self.session)
        data =await dal.Get(id)
        skuDal = ProductSkuDal(self.session)
        skus = await skuDal.GetBySpuId(id)
        data.skus = skus
        return data
    async def UpdateByJsonData(self,jsonData):
        dal = ProductSpuDal(self.session)
        data = await dal.UpdateByJsonData(jsonData)
        skus = jsonData.get('skus')
        skuDal = ProductSkuDal(self.session)
        for sku in skus:
            await skuDal.UpdateByJsonData(sku)
    async def GetCommentList(self,search,PageIndex, PageLimit)->tuple[List[ProductComment],int]:
        dal = ProductCommentDal(self.session)
        datas,total =await dal.Search(search,PageIndex, PageLimit)

        # 查询SKU信息并填充skuProperties
        if datas:
            sku_ids = [comment.skuId for comment in datas if comment.skuId]
            if sku_ids:
                skuDal = ProductSkuDal(self.session)
                skus = await skuDal.GetByIds(sku_ids)
                # 创建SKU ID到properties的映射
                sku_map = {sku.id: sku.properties for sku in skus}
                # 填充每个评论的skuProperties
                for comment in datas:
                    if comment.skuId and comment.skuId in sku_map:
                        comment.skuProperties = sku_map[comment.skuId]

        return datas,total