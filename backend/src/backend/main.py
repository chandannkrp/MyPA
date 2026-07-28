from fastapi import FastAPI
from backend.core.config import settings
from contextlib import asynccontextmanager
from backend.core.logging import logger
from backend.api.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting MyPA Backend")
    yield
    logger.info("Stopping MyPA Backend")

app = FastAPI(
    title="MY-PA API",
    version="1.0.0",
    lifespan=lifespan,
    );


app.include_router(health_router)
           
