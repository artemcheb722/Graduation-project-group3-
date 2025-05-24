from fastapi import FastAPI

from settings import settings


def get_application() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG)

    return app