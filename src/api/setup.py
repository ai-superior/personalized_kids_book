from fastapi import FastAPI, APIRouter
from starlette.staticfiles import StaticFiles

from api.routes.assets import router as assets_router
from api.routes.health import router as health_router
from api.routes.orders import router as leads_router
from api.routes.previews import router as previews_router
from settings import SETTINGS


def create_fastapi_app():
    public_routes = APIRouter(tags=["public"])
    public_routes.include_router(health_router)
    public_routes.include_router(leads_router)
    public_routes.include_router(assets_router)
    public_routes.include_router(previews_router)

    app = FastAPI(
        docs_url="/docs" if SETTINGS.debug else None,
        openapi_url="/openapi.json" if SETTINGS.debug else None,
        redoc_url=None,
    )
    app.include_router(public_routes)

    # Upload the files to S3 bucket instead of storing them here
    app.mount(
        "/public",
        # StaticFiles(directory="/public"),
        StaticFiles(directory="/home/subra/Documents/personalized_kids_book/public"),
        name="public",
    )

    return app
