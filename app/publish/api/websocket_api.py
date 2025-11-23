from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json,os
import asyncio
from pydantic import BaseModel
from app.database import redisClient
from kxy.framework.util import SUtil
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)
ip = SUtil.get_local_ip()

WORKER_ID = f"{ip}:{os.getpid()}"  # 或更独特值
router = APIRouter()

class Message(BaseModel):
    id: str
    data: str
    type: str
    result: str =''
    
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        # 存储客户端ID与WebSocket的映射关系
        self.client_connections: Dict[str, WebSocket] = {}
    async def recive_message(self, websocket: WebSocket):
        while True:
            try:
                message = await websocket.receive_text()
                msg=Message(**json.loads(message))
                logger.debug(f"Received task id {msg.id} message: {msg.result}")
                # await self.broadcast(message)
            except WebSocketDisconnect:
                self.disconnect(websocket)
                break

    async def connect(self,token:str, clientId:str, websocket: WebSocket):
        # Accept first to complete the WebSocket handshake before doing other operations
        await websocket.accept()

        # Only register and add to active list after accept so the connection is live
        self.active_connections.append(websocket)
        if token=='sjdklfsioe' and clientId:
            await self.register_client(clientId, websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        # 从client_connections中移除
        client_id = None
        for cid, ws in self.client_connections.items():
            if ws == websocket:
                client_id = cid
                break
        
        if client_id:
            del self.client_connections[client_id]

    async def broadcast(self, message: dict):
        # 创建一个连接列表的副本，以防在迭代过程中列表发生变化
        connections = list(self.active_connections)
        for connection in connections:
            try:
                # 确保发送的消息是JSON格式
                if isinstance(message, dict):
                    await connection.send_text(json.dumps(message, ensure_ascii=False))
                else:
                    # 如果不是字典类型，包装成标准格式
                    await connection.send_text(json.dumps({"type": "message", "data": message}, ensure_ascii=False))
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                self.disconnect(connection)
    async def worker_channel_loop(self):
        ps = redisClient.client.pubsub()
        await ps.subscribe(f"ws:worker:{WORKER_ID}")
        async for msg in ps.listen():
            if msg['type'] != 'message': continue
            data = json.loads(msg['data'])
            info = Message(**data)
            await self.send_message_to_client(info)
    # 注册客户端
    async def register_client(self, client_id: str, websocket: WebSocket):
        self.client_connections[client_id] = websocket
        logger.info(f"Client registered: {client_id}")
        await redisClient.set(f"ws:client:{client_id}", WORKER_ID)
    
    # 获取特定客户端的WebSocket连接
    def get_client(self, client_id: str) -> WebSocket:
        return self.client_connections.get(client_id)
    
    # 向特定客户端发送消息
    async def send_message_to_client(self, message: Message):
        websocket = self.get_client(message.id)
        if websocket and websocket in self.active_connections:
            try:
                # 检查连接是否仍然开放
                if not websocket.client_state.name == "CONNECTED":
                    logger.info(f"WebSocket connection for client {message.id} is not connected")
                    self.disconnect(websocket)
                    return
                await websocket.send_text(message.model_dump_json())
            except WebSocketDisconnect:
                logger.error(f"WebSocket disconnected when sending message to client {message.id}")
                self.disconnect(websocket)
            except Exception as e:
                logger.error(f"Error sending message to client {message.id}: {e}")
                self.disconnect(websocket)

manager = ConnectionManager()
asyncio.create_task(manager.worker_channel_loop())
@router.post("/sendmessage", response_model=None)
async def send_message(message: Message):
    worker_id = await redisClient.get(f"ws:client:{message.id}")
    if not worker_id:
        return
    await redisClient.client.publish(f"ws:worker:{worker_id.decode()}", message.model_dump_json())
    return {"status": "success"}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: str = None, token: str = None):
    await manager.connect(token, client_id, websocket)
    try:
        await manager.recive_message(websocket)
    finally:
        manager.disconnect(websocket)