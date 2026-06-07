import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.config import config
from app.logger import logger
from app.schema import UserRequest, UserResponse
from app.services.agent import agentic_service

app = FastAPI(
    title="HACCP Agentic AI Service API",
    version="0.1.0",
    docs_url=(None if config.APP_ENV == "prd" else "/docs"),
    redoc_url=(None if config.APP_ENV == "prd" else "/redoc"),
)

allow_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.middleware("http")
async def log_requests_and_execution_time(request: Request, call_next):
    start_time = time.perf_counter()

    logger.info(f"HTTP Inbound [{request.method}] {request.url.path}")

    response = await call_next(request)

    process_time = time.perf_counter() - start_time
    logger.info(
        f"HTTP Outbound [{request.method}] {request.url.path} - Status: {response.status_code} - Taken: {process_time:.2f}s"
    )
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.critical(
        f"Internal server error occurred: {request.url.path} | exception: {exc}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "서버 내부에서 예상치 못한 오류가 발생했습니다.",
        },
    )


@app.post("/api/v1/chat", response_model=UserResponse, tags=["Agent"])
def chat(request: UserRequest):

    return agentic_service.chat(request=request)
