from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.usecases.model_usecase import model_usecase
from src.core.logger.logger import logger
from numpy import frombuffer, uint8
import cv2


router = APIRouter()


@router.websocket("/ws/detect")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = id(websocket)
    logger.info(f"Client {client_id} connected")
    
    try:
        while True:
            data = await websocket.receive_bytes()
            np_array = frombuffer(data, uint8)
            frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            is_fire = await model_usecase.detect(frame)

            await websocket.send_text(f"Fire detected: {is_fire}")

    except WebSocketDisconnect as e:
        logger.info(f"Client {client_id} disconnected: {e.code}, {e.reason}")
    
    except Exception as e:
        logger.error(f"Unexpected error with client {client_id}: {str(e)}")

    finally:
        logger.info(f"Client {client_id} connection closed")

