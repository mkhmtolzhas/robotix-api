from fastapi import APIRouter, Depends, File, HTTPException
from src.usecases.model_usecase import ModelUseCase, get_model_usecase
from src.schemas.coordinates import Coordinates
router = APIRouter(prefix="/image", tags=["image"])


@router.post("/upload", response_model=Coordinates)
async def upload_image(
    file: bytes = File(...),
    usecase: ModelUseCase = Depends(get_model_usecase),
):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    try:
        result = await usecase.detect_fire_coordinates(file)

        if result is None:
            return Coordinates(verdict="no_fire", coordinates=None)

        x1, y1, x2, y2 = result
        coordinates = (x1, y1, x2, y2)
        return Coordinates(verdict="fire", coordinates=coordinates)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
