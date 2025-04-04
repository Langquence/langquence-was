from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes.routes import router
from app.config.app_config import settings
from app.common.utils.logger import get_logger
from app.common.exception.base_exception import BaseException
from app.common.exception.global_exception_handler import base_exception_handler, http_exception_handler, validation_exception_handler, global_exception_handler

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

app.add_exception_handler(BaseException, base_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

@app.get("/")
async def root():
    return {"message": "Welcome to Langquence API", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}