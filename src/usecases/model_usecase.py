import cv2
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Tuple
from src.inference.model_inference import ModelInference, model_inference
from numpy import frombuffer, uint8
import asyncio



class ModelUseCase(ABC):
    @abstractmethod
    async def detect(self, data: bytes) -> bool:
        pass

    @abstractmethod
    async def detect_with_image(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    async def detect_fire_coordinates(self, data: bytes) -> Tuple[int, int, int, int]:
        pass

class ModelUseCaseImpl:
    def __init__(self, inference: ModelInference):
        self.inference = inference

    async def detect(self, data: bytes) -> bool:
        np_array = frombuffer(data, uint8)
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        return await asyncio.to_thread(self.inference.detect_fire, frame)
    
    async def detect_with_image(self, data: bytes) -> bytes:
        np_array = frombuffer(data, uint8)
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        result = await asyncio.to_thread(self.inference.detect_fire_with_image, frame)
        _, buffer = cv2.imencode('.jpg', result)
        return buffer.tobytes()
    
    async def detect_fire_coordinates(self, data: bytes) -> Tuple[int, int, int, int]:
        np_array = frombuffer(data, uint8)
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        result = await asyncio.to_thread(self.inference.detect_fire_coordinates, frame)
        if result is not None:
            x1, y1, x2, y2 = result
            return (x1, y1, x2, y2)
        return None


async def get_model_usecase() -> AsyncGenerator[ModelUseCase, None]:
    yield ModelUseCaseImpl(model_inference)