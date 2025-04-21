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

    
@router.websocket("/ws/detect/image")
async def websocket_endpoint_with_image(
    websocket: WebSocket,
    model_usecase: ModelUseCase = Depends(get_model_usecase)
):
    await websocket.accept()
    client_id = id(websocket)
    logger.info(f"Client {client_id} connected")
    
    try:
        while True:
            data = await websocket.receive_bytes()

            result = await model_usecase.detect_with_image(data)

            await websocket.send_bytes(result)

    except WebSocketDisconnect as e:
        logger.info(f"Client {client_id} disconnected: {e.code}, {e.reason}")
    
    except Exception as e:
        logger.error(f"Unexpected error with client {client_id}: {str(e)}")

    finally:
        logger.info(f"Client {client_id} connection closed")



@router.websocket("/ws/detect/coordinates")
async def websocket_endpoint_with_coordinates(
    websocket: WebSocket,
    model_usecase: ModelUseCase = Depends(get_model_usecase)
):
    await websocket.accept()
    client_id = id(websocket)
    logger.info(f"Client {client_id} connected")
    
    try:
        while True:
            data = await websocket.receive_bytes()

            result = await model_usecase.detect_fire_coordinates(data)
            print(result)

            if result is not None:
                x1, y1, x2, y2 = result
                await websocket.send_text(f"Fire coordinates: ({x1}, {y1}, {x2}, {y2})")
            else:
                await websocket.send_text("No fire detected")

    except WebSocketDisconnect as e:
        logger.info(f"Client {client_id} disconnected: {e.code}, {e.reason}")
    
    except Exception as e:
        logger.error(f"Unexpected error with client {client_id}: {str(e)}")

    finally:
        logger.info(f"Client {client_id} connection closed")
