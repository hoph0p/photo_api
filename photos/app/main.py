from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import media_settings, api_setting, app_settings
from api_v1 import router as router_v1


def get_application() -> FastAPI:
    app = FastAPI(
        title=app_settings.app_name
    )

    storage_dir = media_settings.storage_root
    storage_dir.mkdir(parents=True, exist_ok=True)

    app.mount(
        media_settings.storage_url,
        StaticFiles(directory=storage_dir),
        name="storage"
    )

    app.include_router(
        router=router_v1,
        prefix=api_setting.api_prefix
    )
    return app


app = get_application()
