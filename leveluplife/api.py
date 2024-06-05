from urllib.request import Request
from leveluplife.routes.user import router as user_router
from leveluplife.routes.task import router as task_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from loguru import logger
from leveluplife.models.error import BaseError


def create_app(lifespan) -> FastAPI:
    origins = ["*"]
    app = FastAPI(title="LevelUpLife", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(user_router)
    app.include_router(task_router)

    @app.exception_handler(BaseError)
    async def exception_handler(request: Request, exc: BaseError) -> JSONResponse:
        logger.error(f"{type(exc).__name__}: {exc.message}", exc_info=exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.message,
                "name": exc.name,
                "status_code": exc.status_code,
            },
        )

    return app
