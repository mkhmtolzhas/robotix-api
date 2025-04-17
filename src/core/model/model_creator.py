from abc import ABC, abstractmethod
from ultralytics import YOLO

class ModelCreator(ABC):
    @abstractmethod
    def model_factory(self) -> YOLO:
        pass
