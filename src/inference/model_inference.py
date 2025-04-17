from src.core.model.model_creator import ModelCreator
from src.core.model.yolo_creator import yolo_creator
from abc import ABC, abstractmethod
from numpy import ndarray


class ModelInference(ABC):
    @abstractmethod
    def detect_fire(self, frame: ndarray) -> bool:
        pass


class ModelInferenceImpl(ModelInference):
    def __init__(self, model: ModelCreator):
        self.model = model.model_factory()

    def detect_fire(self, frame: ndarray) -> bool:
        results = self.model(frame)
        return len(results[0].boxes) > 0


model_inference = ModelInferenceImpl(yolo_creator)