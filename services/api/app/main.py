import logging
from pythonjsonlogger import jsonlogger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.api.app.api.routes import router
from services.api.app.core.config import settings

handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[handler])

app = FastAPI(title=settings.app_name, version="3.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name, "environment": settings.environment}
