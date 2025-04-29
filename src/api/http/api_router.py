from fastapi import APIRouter
from .image.image import router as image_router


router = APIRouter(prefix="/api")



router.include_router(image_router)


@router.get("/")
async def root():
    return {"message": "Hello World"}
