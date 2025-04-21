from src.core.model.model_creator import ModelCreator
from src.core.model.yolo_creator import yolo_creator
from abc import ABC, abstractmethod
from typing import Tuple, Optional
from numpy import ndarray


class ModelInference(ABC):
    @abstractmethod
    def detect_fire(self, frame: ndarray) -> bool:
        pass

    @abstractmethod
    def detect_fire_with_image(self, frame: ndarray) -> ndarray:
        pass

    @abstractmethod
    def detect_fire_coordinates(self, frame: ndarray) -> Tuple[Optional[Tuple[int, int, int, int]]]:
        pass


class ModelInferenceImpl(ModelInference):
    def __init__(self, model: ModelCreator):
        self.model = model.model_factory()

    def detect_fire(self, frame: ndarray) -> bool:
        results = self.model(frame)
        return len(results[0].boxes) > 0
    
    def detect_fire_with_image(self, frame: ndarray) -> ndarray:
        results = self.model(frame)
        return results[0].plot()
    
    def detect_fire_coordinates(self, frame: ndarray) -> Optional[Tuple[int, int, int, int]]:
        results = self.model(frame)
        boxes = results[0].boxes

        if len(boxes) > 0:
            box = boxes[0].xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = map(int, box)
            return (x1, y1, x2, y2)

        return None

        



model_inference = ModelInferenceImpl(yolo_creator)

