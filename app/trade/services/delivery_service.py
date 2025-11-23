from typing import Dict, List, Union
from kxy.framework.base_service import BaseService
from kxy.framework.friendly_exception import FriendlyException

from app.trade.dal.trade_delivery_express_template_dal import TradeDeliveryExpressTemplateDal
from app.trade.dal.trade_delivery_express_template_charge_dal import TradeDeliveryExpressTemplateChargeDal
from app.trade.dal.trade_delivery_express_template_free_dal import TradeDeliveryExpressTemplateFreeDal
from app.trade.dal.trade_delivery_pick_up_store_dal import TradeDeliveryPickUpStoreDal
from app.trade.models.trade_delivery_express_template import TradeDeliveryExpressTemplate
from app.trade.models.trade_delivery_express_template_charge import TradeDeliveryExpressTemplateCharge
from app.trade.models.trade_delivery_express_template_free import TradeDeliveryExpressTemplateFree
from app.trade.models.trade_delivery_pick_up_store import TradeDeliveryPickUpStore
from app.system.dal.system_users_dal import SystemUsersDal
from app.system.models.system_users import SystemUsers

class DeliveryService(BaseService):
    async def get_express_template_by_id(self, template_id: int) -> TradeDeliveryExpressTemplate:
        """
        根据id获取运费模板详情，包括计费规则和包邮规则
        :param template_id: 运费模板ID
        :return: 运费模板对象（包含charges和frees属性）
        """
        # 查询运费模板基本信息
        template_dal = TradeDeliveryExpressTemplateDal(self.session)
        template = await template_dal.GetExist(template_id)

        # 查询计费规则
        charge_dal = TradeDeliveryExpressTemplateChargeDal(self.session)
        charges = await charge_dal.GetByTemplateId(template_id)
        template.charges = charges

        # 查询包邮规则
        free_dal = TradeDeliveryExpressTemplateFreeDal(self.session)
        frees = await free_dal.GetByTemplateId(template_id)
        template.frees = frees

        return template

    async def create_express_template(self, data: Dict) -> TradeDeliveryExpressTemplate:
        """
        创建运费模板，包括计费规则和包邮规则
        :param data: 运费模板数据，格式：{
            "name": "模板名称",
            "chargeMode": 1,
            "sort": 0,
            "charges": [{"areaIds": [110101, 110102], "startCount": 2, "startPrice": 500, "extraCount": 5, "extraPrice": 1000}],
            "frees": [{"areaIds": [110101, 110102], "freeCount": 1, "freePrice": 100}]
        }
        :return: 创建的运费模板对象（包含charges和frees属性）
        """
        # 提取charges和frees数据
        charges_data = data.pop('charges', [])
        frees_data = data.pop('frees', [])

        # 创建运费模板基本信息
        template_dal = TradeDeliveryExpressTemplateDal(self.session)
        template = await template_dal.AddByJsonData(data)

        # 批量创建计费规则
        charge_dal = TradeDeliveryExpressTemplateChargeDal(self.session)
        charge_entities = []
        for charge_item in charges_data:
            # 创建实体对象
            charge_entity = TradeDeliveryExpressTemplateCharge()

            # 添加模板ID和计费模式
            charge_item['templateId'] = template.id
            charge_item['chargeMode'] = data.get('chargeMode')

            # 初始化实体
            charge_entity.InitInsertEntityWithJson(charge_item)
            charge_entity.deleted = 0
            charge_entities.append(charge_entity)

        # 批量插入计费规则
        if charge_entities:
            await charge_dal.BatchInsert(charge_entities)
        charges = charge_entities

        # 批量创建包邮规则
        free_dal = TradeDeliveryExpressTemplateFreeDal(self.session)
        free_entities = []
        for free_item in frees_data:
            # 创建实体对象
            free_entity = TradeDeliveryExpressTemplateFree()

            # 添加模板ID
            free_item['templateId'] = template.id

            # 初始化实体
            free_entity.InitInsertEntityWithJson(free_item)
            free_entity.deleted = 0
            free_entities.append(free_entity)

        # 批量插入包邮规则
        if free_entities:
            await free_dal.BatchInsert(free_entities)
        frees = free_entities

        # 将charges和frees填充到模板对象
        template.charges = charges
        template.frees = frees

        return template

    async def update_express_template(self, template_id: int, data: Dict) -> TradeDeliveryExpressTemplate:
        """
        更新运费模板,包括计费规则和包邮规则
        :param template_id: 运费模板ID
        :param data: 运费模板数据,格式:{
            "name": "模板名称",
            "chargeMode": 1,
            "sort": 0,
            "charges": [{"areaIds": [110101, 110102], "startCount": 2, "startPrice": 500, "extraCount": 5, "extraPrice": 1000}],
            "frees": [{"areaIds": [110101, 110102], "freeCount": 1, "freePrice": 100}]
        }
        :return: 更新后的运费模板对象(包含charges和frees属性)
        """
        # 提取charges和frees数据
        charges_data = data.pop('charges', [])
        frees_data = data.pop('frees', [])

        # 查询并更新运费模板基本信息
        template_dal = TradeDeliveryExpressTemplateDal(self.session)
        template = await template_dal.GetExist(template_id)

        # 更新模板基本信息
        data['id'] = template_id
        template = await template_dal.UpdateByJsonData(data)

        # 删除旧的计费规则
        charge_dal = TradeDeliveryExpressTemplateChargeDal(self.session)
        await charge_dal.DeleteByTemplateId(template_id)

        # 批量创建新的计费规则
        charge_entities = []
        for charge_item in charges_data:
            # 创建实体对象
            charge_entity = TradeDeliveryExpressTemplateCharge()

            # 添加模板ID和计费模式
            charge_item['templateId'] = template.id
            charge_item['chargeMode'] = data.get('chargeMode')

            # 初始化实体
            charge_entity.InitInsertEntityWithJson(charge_item)
            charge_entity.deleted = 0
            charge_entities.append(charge_entity)

        # 批量插入计费规则
        if charge_entities:
            await charge_dal.BatchInsert(charge_entities)
        charges = charge_entities

        # 删除旧的包邮规则
        free_dal = TradeDeliveryExpressTemplateFreeDal(self.session)
        await free_dal.DeleteByTemplateId(template_id)

        # 批量创建新的包邮规则
        free_entities = []
        for free_item in frees_data:
            # 创建实体对象
            free_entity = TradeDeliveryExpressTemplateFree()

            # 添加模板ID
            free_item['templateId'] = template.id

            # 初始化实体
            free_entity.InitInsertEntityWithJson(free_item)
            free_entity.deleted = 0
            free_entities.append(free_entity)

        # 批量插入包邮规则
        if free_entities:
            await free_dal.BatchInsert(free_entities)
        frees = free_entities

        # 将charges和frees填充到模板对象
        template.charges = charges
        template.frees = frees

        return template

    async def delete_express_template(self, template_id: int):
        """
        删除运费模板,包括关联的计费规则和包邮规则
        :param template_id: 运费模板ID
        """
        # 验证模板是否存在
        template_dal = TradeDeliveryExpressTemplateDal(self.session)
        await template_dal.GetExist(template_id)

        # 删除计费规则
        charge_dal = TradeDeliveryExpressTemplateChargeDal(self.session)
        await charge_dal.DeleteByTemplateId(template_id)

        # 删除包邮规则
        free_dal = TradeDeliveryExpressTemplateFreeDal(self.session)
        await free_dal.DeleteByTemplateId(template_id)

        # 删除模板本身
        await template_dal.Delete(template_id)

    async def bind_verify_users(self, store_id: int, verify_user_ids: List[int]) -> TradeDeliveryPickUpStore:
        """
        绑定核销用户到自提门店

        :param store_id: 门店ID
        :param verify_user_ids: 核销用户ID数组
        :return: 更新后的门店实体
        """
        # 查询门店是否存在
        store_dal = TradeDeliveryPickUpStoreDal(self.session)
        store = await store_dal.GetExist(store_id)
        # 更新门店的核销用户信息
        store.verifyUserIds = verify_user_ids
        await store_dal.Update(store)
        return store
    async def get_store(self, store_id: int):
        dal = TradeDeliveryPickUpStoreDal(self.session)
        data =await dal.Get(store_id)
        verify_users_data = []
        if data.verifyUserIds:
            user_dal = SystemUsersDal(self.session)
            users = await user_dal.GetUserByIds(data.verifyUserIds)

            for user in users:
                verify_users_data.append({
                    "id": user.id,
                    "nickname": user.nickname,
                    "avatar": user.avatar
                })

        # 更新门店的核销用户信息
        data.verifyUsers = verify_users_data
        return data
