from ultralytics import YOLO
from ultralytics.nn.tasks import DetectionModel
import torch
from .model_creator import ModelCreator

class YoloCreator(ModelCreator):
    def __init__(self, detection_model: DetectionModel):
        self.detection_model = detection_model
        torch.load('best.pt', weights_only=False)
        self.detection_model = YOLO('best.pt')

    def setup_model(self, conf: float, iou: float, max_det: int):
        self.detection_model.overrides['conf'] = conf
        self.detection_model.overrides['iou'] = iou
        self.detection_model.overrides['max_det'] = max_det

    def model_factory(self) -> DetectionModel:
        return self.detection_model



yolo_creator = YoloCreator(DetectionModel())