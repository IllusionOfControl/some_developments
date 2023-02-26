from typing import Optional, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Cookie
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import queue
import time


app = FastAPI()
app.queue_system = queue.Queue()
app.queue_limit = 5

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8000",
    "http://127.0.0.1:8080",
    "http://0.0.0.0:8080",
]


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str, websocket: WebSocket):
        del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: str):
        connection: WebSocket = self.active_connections[client_id]
        await connection.send_text(message)

    async def broadcast(self, message: str):
        for client_id in self.active_connections.keys():
            connection = self.active_connections[client_id]
            await connection.send_text(message)


manager = ConnectionManager()


async def websocket_queue_handler():
    for i in range(app.queue_limit):
        if not app.queue_system.empty():
            obj = app.queue_system.get_nowait()
            if obj['client_id'] in manager.active_connections:
                await manager.send_personal_message(f"You wrote: {obj['message']}", obj['client_id'])
                await manager.broadcast(f"Client #{obj['client_id']} says: {obj['message']}")


app.scheduler = AsyncIOScheduler()
app.scheduler.add_job(websocket_queue_handler, 'interval', seconds=1)
app.scheduler.start()


with open("index.html", "r") as html_index:
    html = html_index.read()


@app.get("/")
async def index():
    response = HTMLResponse(html)
    response.set_cookie('client_id', str(time.time_ns()))
    return response


@app.post("/")
async def create_message(message: Dict[str, str], client_id: Optional[str] = Cookie(None)):
    if client_id:
        app.queue_system.put({"message": message['text'], "client_id": client_id})
        return {"success": True}
    else:
        return {"success": False}


@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    await manager.broadcast(f"Client #{client_id} connected")
    try:
        while True:
            message = await websocket.receive()
            if message["type"] == "websocket.disconnect":
                break
    except WebSocketDisconnect:
        manager.disconnect(client_id, websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, workers=1, loop="asyncio")
