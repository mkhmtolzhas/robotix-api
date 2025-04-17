import cv2
from abc import ABC, abstractmethod
from typing import AsyncGenerator
from src.inference.model_inference import ModelInference, model_inference
from numpy import frombuffer, uint8
import asyncio


class ModelUseCase(ABC):
    @abstractmethod
    async def detect(self, data: bytes) -> bool:
        pass

class ModelUseCaseImpl:
    def __init__(self, inference: ModelInference):
        self.inference = inference

    async def detect(self, data: bytes) -> bool:
        np_array = frombuffer(data, uint8)
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        return await asyncio.to_thread(self.inference.detect_fire, frame)
    


async def get_model_usecase() -> AsyncGenerator[ModelUseCase, None]:
    yield ModelUseCaseImpl(model_inference)