from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import media_settings, api_setting
from .api_v1 import router as router_v1

app = FastAPI(
    title="Photo Processor"
)

storage_dir = media_settings.storage_root
storage_dir.mkdir(parents=True, exist_ok=True)

app.mount(
    media_settings.media_ulr,
    StaticFiles(directory=storage_dir),
    name="storage"
)

app.include_router(
    router=router_v1,
    prefix=api_setting.api_prefix
)
