import json
from redis.asyncio import Redis,ConnectionPool

from app.global_var import Gkey, Keys 

class RedisClient():
    def __init__(self,host,port=6379,password=None,db=0):
        self.redis_pool:ConnectionPool = ConnectionPool(host=host,
    port=port,
    db=db,
    password=password,
    max_connections=100
)
        self.client = Redis(connection_pool=self.redis_pool)
    def _gen_key(self,key,*args):
        if isinstance(key,Keys):
            key = Gkey(key,*args)
        return key
    async def get_string(self,key,*args):
        key = self._gen_key(key,*args)
        v = await self.client.get(key)
        if v:
            return v.decode('utf-8')
        return None
    
    async def get_json(self,key,*args):
        key = self._gen_key(key,*args)
        v = await self.client.get(key)
        if v:
            return json.loads(v)
        return None
    async def get_int(self,key,*args):
        key = self._gen_key(key,*args)
        return await self.client.get(key)
    async def set_int(self,key,value,**kwargs):
        return await self.client.set(key,value,**kwargs)
    async def set_string(self,key,value,**kwargs):
        return await self.client.set(key,value,**kwargs)
    async def delete(self,key):
        return await self.client.delete(key)
    async def set(self,key,value,*args,**kwargs):
        return await self.client.set(key,value,*args,**kwargs)
    async def set_json(self,key,value,*args,**kwargs):
        return await self.client.set(key,json.dumps(value),*args,**kwargs)
    
    async def get(self,key,*args):
        key = self._gen_key(key,*args)
        return await self.client.get(key)