from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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

    # @app.exception_handler(BaseError)
    # async def exception_handler(request: Request, exc: BaseError) -> JSONResponse:
    #     return JSONResponse(
    #         status_code=exc.status_code,
    #         content={
    #             "message": exc.message,
    #             "name": exc.name,
    #             "status_code": exc.status_code,
    #         },
    #     )

    return app
