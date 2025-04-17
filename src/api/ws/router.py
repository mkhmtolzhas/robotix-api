from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from src.usecases.model_usecase import ModelUseCase, get_model_usecase
from src.core.logger.logger import logger


router = APIRouter()


@router.websocket("/ws/detect")
async def websocket_endpoint(
    websocket: WebSocket,
    model_usecase: ModelUseCase = Depends(get_model_usecase)
):
    await websocket.accept()
    client_id = id(websocket)
    logger.info(f"Client {client_id} connected")
    
    try:
        while True:
            data = await websocket.receive_bytes()

            is_fire = await model_usecase.detect(data)

            await websocket.send_text(f"Fire detected: {is_fire}")

    except WebSocketDisconnect as e:
        logger.info(f"Client {client_id} disconnected: {e.code}, {e.reason}")
    
    except Exception as e:
        logger.error(f"Unexpected error with client {client_id}: {str(e)}")

    finally:
        logger.info(f"Client {client_id} connection closed")

