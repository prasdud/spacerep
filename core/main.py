from fastapi import FastAPI
import dotenv
import logging as log
from core.api.routes import router

log.basicConfig(level=log.INFO)
log.info("Starting fastAPI application...")

envLoaded = dotenv.load_dotenv()
if envLoaded:
    log.info("Environment variables loaded from .env file")
else:
    log.warning("No .env file found or failed to load, using system environment variables")

app = FastAPI()
log.info("FastAPI application instance created")

app.include_router(router)
log.info("API routes registered successfully!")
log.info("Application setup complete and ready to serve requests.")