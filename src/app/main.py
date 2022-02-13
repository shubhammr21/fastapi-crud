from fastapi import FastAPI
from app.api import ping, notes
from app.db import engine, database, metadata
from app.config.settings import settings
from app.api.routers import api_router
from starlette.middleware.cors import CORSMiddleware
metadata.create_all(engine)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(api_router, prefix=settings.API_V1_STR)
