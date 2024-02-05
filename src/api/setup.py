from fastapi import FastAPI, APIRouter

from api.routes.health import router as health_router

from settings import SETTINGS


def create_fastapi_app():
    public_routes = APIRouter(tags=["public"])
    public_routes.include_router(health_router)

    app = FastAPI(
        docs_url="/docs" if SETTINGS.debug else None,
        openapi_url="/openapi.json" if SETTINGS.debug else None,
        redoc_url=None,
    )
    app.include_router(public_routes)

    return app
