from pydantic import BaseModel, Field
from typing import Tuple, Optional


class Coordinates(BaseModel):
    verdict: str = Field(default="fire", description="Verdict of the fire detection")
    coordinates: Optional[Tuple[int, int, int, int]] = Field(
        default=None,
        description="Coordinates of the fire detection in the format (x1, y1, x2, y2)",
    )