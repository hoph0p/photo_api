"""App configuration"""
from pathlib import Path
from pydantic_settings import BaseSettings


class DBSetting(BaseSettings):
    db_url: str = 'postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/photo_api_db'
    db_echo: bool = True


db_settings = DBSetting()


class AppSetting(BaseSettings):
    app_name: str = 'Photo API'


app_settings = AppSetting()


class ApiSetting(BaseSettings):
    api_prefix: str = '/api/v1'


api_setting = ApiSetting()


class MediaSetting(BaseSettings):
    media_root: Path = Path('media')
    media_url: str = '/media'
    storage_url: str = media_url + '/storage'
    storage_root: Path = Path(media_root, 'storage')


media_settings = MediaSetting()


class S3Settings(BaseSettings):
    endpoint_url: str = ''


s3_settings = S3Settings()
