import httpx
from typing import Dict, Optional

class HttpxClientHelper:
    @staticmethod
    async def get(url: str, 
                       params: Optional[Dict] = None, 
                       **kwargs) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            return await client.get(url, params=params, **kwargs)
    @staticmethod
    async def post(url: str, 
                        data: Optional[Dict] = None, 
                        json: Optional[Dict] = None, 
                        **kwargs) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            return await client.post(url, data=data, json=json, **kwargs)