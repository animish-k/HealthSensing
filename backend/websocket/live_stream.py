from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.websocket.manager import ConnectionManager


router = APIRouter(tags=["stream"])
manager = ConnectionManager()


@router.websocket("/ws/readings")
async def readings_stream(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except RuntimeError:
        manager.disconnect(websocket)
        raise