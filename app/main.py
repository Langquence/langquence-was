import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config.app_config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(router, prefix=settings.API_PREFIX)

# deprecated 되었음. fast api lifespan으로 대체
# @app.on_event("startup")
# async def startup_event():
#     logger.info("Starting up Langquence API server")

# @app.on_event("shutdown")
# async def shutdown_event():
#     logger.info("Shutting down Langquence API server")

@app.get("/")
async def root():
    return {"message": "Welcome to Langquence API", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)