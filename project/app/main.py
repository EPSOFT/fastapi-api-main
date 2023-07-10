import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import ping, summaries
from app.db import init_db

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    """
    Initialises the FastAPIapp
        - Includes tags for grouping operations (https://swagger.io/docs/specification/grouping-operations-with-tags/))
    ---------------------------
    Routes:
        ping -> pong(): returns environment (dev, stage, prod) & testing config (y/n) of active pydantic BaseSetting
        summaries: define a handler that expects a payload (SummaryPayloadSchema), w/ a URL.
    """
    application = FastAPI()

    application.include_router(ping.router)
    application.mount("/static", StaticFiles(directory="static"), name="static")
    application.include_router(
        summaries.router, prefix="/summaries", tags=["summaries"]
    )
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
