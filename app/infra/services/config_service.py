from app.database import redisClient
from app.global_var import Gkey, Keys
from app.infra.dal.infra_config_dal import InfraConfigDal
from app.system.services.base_service import BaseService
from typing import Dict, Callable, Any, List
import asyncio


class ConfigService(BaseService):
    _watchers: Dict[str, List[Callable[[str, Any], None]]] = {}

    def __init__(self, session, **kwargs):
        super().__init__(session, **kwargs)

    def watch(cls, key: str, callback: Callable[[str, Any], None]):
        """
        注册一个观察者函数，当指定的配置项被更新时会调用该函数
        
        Args:
            key: 配置项键名
            callback: 回调函数，接受两个参数：配置项键名和新值
        """
        watchers = cls._watchers.setdefault(key, [])
        if callback not in watchers:
            watchers.append(callback)

    async def Get(self, key) -> str:
        dal = InfraConfigDal(self.session)
        return await dal.GetByKey(key)

    async def GetByCache(self, key, ex=3600) -> str:
        cache_key = Gkey(Keys.CONFIG_VALUE, key)
        value = await redisClient.get_string(cache_key)
        if value is not None:
            return value
        value = await self.Get(key)
        if value is not None:
            await redisClient.set_string(cache_key, value, ex=ex)
        return value

    async def update(self, data):
        dal = InfraConfigDal(self.session)
        result = await dal.UpdateByJsonData(data)
        
        # 检查是否有观察者注册在这个配置项上，如果有则触发回调
        callbacks = self.__class__._watchers.get(result.key, [])
        for callback in callbacks:
            # 异步执行回调函数避免阻塞主流程
            asyncio.create_task(
                self._execute_watcher_callback(result.key, result.value, callback)
            )
        
        return result
    
    async def _execute_watcher_callback(
        self, key: str, new_value: Any, callback: Callable[[str, Any], None]
    ):
        """
        执行观察者的回调函数
        
        Args:
            key: 配置项键名
            new_value: 新的配置值
        """
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(key, new_value)
            else:
                callback(key, new_value)
        except Exception as e:
            self.logger.error(f"执行配置 {key} 的观察者回调函数时发生错误: {e}")
