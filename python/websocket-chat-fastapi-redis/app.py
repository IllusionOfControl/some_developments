import os
from typing import Optional, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Cookie
from fastapi.responses import HTMLResponse
import asyncio
import uvicorn
import time
import json
import aioredis


REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1")


app = FastAPI()
redis = aioredis.redis = aioredis.from_url(
        REDIS_URL, encoding="utf-8", decode_responses=True
    )

with open("index.html", "r") as html_index:
    html = html_index.read()


origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8000",
    "http://127.0.0.1:8080",
    "http://0.0.0.0:8080",
]


class RoomManager:
    def __init__(self, room_name):
        self._name = room_name
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        del self.active_connections[client_id]

    async def publish_message(self, message):
        await redis.publish(self._name, message)

    async def subscribe_to_messages(self):
        async with redis.pubsub() as pubsub:
            await pubsub.subscribe(self._name)
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    message = message["data"]
                    await self.broadcast(message)

    async def broadcast(self, message):
        for client_id in self.active_connections.keys():
            websocket = self.active_connections[client_id]
            await websocket.send_text(message)


manager = RoomManager("global_chat")


@app.get("/")
async def index():
    response = HTMLResponse(html)
    response.set_cookie('client_id', str(time.time_ns()))
    return response


@app.post("/")
async def create_message(message: Dict[str, str], client_id: Optional[str] = Cookie(None)):
    if client_id:
        await redis.publish("global_chat", json.dumps({"message": message['text'], "client_id": client_id, "type": "broadcast_msg"}))
        return {"success": True}
    else:
        return {"success": False}


@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    await manager.publish_message(json.dumps({
        "client_id": client_id,
        "type": "connected"
    }))
    try:
        while True:
            message = await websocket.receive()
            if message["type"] == "websocket.disconnect":
                manager.disconnect(client_id)
                await websocket.close()
                await manager.broadcast(json.dumps(
                    {"client_id": client_id, "type": "disconnected"}
                ))
                break
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(json.dumps(
            {"client_id": client_id, "type": "disconnected"}
        ))

loop = asyncio.new_event_loop()

config = uvicorn.Config(app=app, loop="asyncio", host="127.0.0.1", port=8000)
server = uvicorn.Server(config)

loop.create_task(server.serve())
loop.create_task(manager.subscribe_to_messages())


if __name__ == "__main__":
    loop.run_forever()
