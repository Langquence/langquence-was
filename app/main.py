from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config.app_config import settings
from app.common.utils.logger import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Langquence API server")
    
    logger.info(f"Application Name: {settings.APP_NAME}")
    logger.info(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
    logger.info(f"API Prefix: {settings.API_PREFIX}")
    logger.info(f"Host: {settings.APP_HOST}:{settings.APP_PORT}")
    logger.info(f"Model: {settings.MODEL_NAME}")

    yield

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {"message": "Welcome to Langquence API", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}