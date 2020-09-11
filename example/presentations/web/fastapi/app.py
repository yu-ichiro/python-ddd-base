import inject
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
# from starlette.staticfiles import StaticFiles
from example.di import sqlite_file_config
from .user import user_router

app = FastAPI(
    title="Example API",
    version="0.1.0",
    description="The API to interact with Example",
    docs_url="/playground",
    redoc_url="/",
)


inject.configure(sqlite_file_config)


def openapi_generator():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
        servers=app.servers,
    )
    if "info" not in openapi_schema:
        openapi_schema["info"] = {}
    # openapi_schema["info"]["x-logo"] = dict(url="/static/standardsign_logo.png")
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# TODO: 適切に設定する
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
    allow_origin_regex=None,
    expose_headers=(),
    max_age=600,
)

app.openapi = openapi_generator
# app.mount("/static", StaticFiles(directory=os.path.join(PROJECT_ROOT, 'static')), name="static")
app.include_router(user_router)
