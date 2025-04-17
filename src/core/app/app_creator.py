from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from src.api.http.api_router import router as api_router
from src.api.ws.router import router as ws_router


class AppCreator:
    def __init__(self) -> None:
        self._app = FastAPI()

    def create_app(self) -> FastAPI:
        return self._app

    def add_router(self, router: APIRouter) -> None:
        self._app.include_router(router)

    def add_cors(self, allow_origins: List[str]) -> None:
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
        
        

app_creator = AppCreator()
app_creator.add_router(api_router)
app_creator.add_router(ws_router)
app_creator.add_cors(allow_origins=["*"])