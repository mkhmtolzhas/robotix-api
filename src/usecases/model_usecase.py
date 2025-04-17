from abc import ABC, abstractmethod
from typing import AsyncGenerator

from src.inference.model_inference import ModelInference, model_inference
from numpy import ndarray
import asyncio


class ModelUseCase(ABC):
    @abstractmethod
    async def detect(self, frame: ndarray) -> bool:
        pass

class ModelUseCaseImpl:
    def __init__(self, inference: ModelInference):
        self.inference = inference

    async def detect(self, frame: ndarray) -> bool:
        return await asyncio.to_thread(self.inference.detect_fire, frame)
    


model_usecase = ModelUseCaseImpl(model_inference)