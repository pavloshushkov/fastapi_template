from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api import router
from api.home.home import home_router
from core.config import config
from core.exceptions import CustomException
from core.fastapi.dependencies import Logging
from core.fastapi.middlewares import (
    AuthenticationMiddleware,
    AuthBackend,
    SQLAlchemyMiddleware,
)


def init_cors(app: FastAPI) -> None:
    # https://fastapi.tiangolo.com/tutorial/middleware/#create-a-middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_routers(app: FastAPI) -> None:
    # https://fastapi.tiangolo.com/tutorial/bigger-applications/#another-module-with-apirouter
    app.include_router(home_router)
    app.include_router(router)


def init_listeners(app: FastAPI) -> None:
    # Exception handler
    # https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def init_middleware(app: FastAPI) -> None:
    # https://fastapi.tiangolo.com/tutorial/middleware/#create-a-middleware
    app.add_middleware(
        AuthenticationMiddleware,
        backend=AuthBackend(),
        on_error=on_auth_error,
    )
    app.add_middleware(SQLAlchemyMiddleware)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Fast API",
        description="Fast API",
        version="1.0.0",  # https://semver.org/lang/uk/
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        dependencies=[Depends(Logging)],  # https://fastapi.tiangolo.com/tutorial/dependencies/#first-steps
    )
    init_routers(app=app)
    init_cors(app=app)  # https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    init_listeners(app=app)
    init_middleware(app=app)
    return app


app = create_app()
