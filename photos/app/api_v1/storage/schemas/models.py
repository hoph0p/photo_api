from datetime import datetime
from pydantic import BaseModel, ConfigDict


class StorageBase(BaseModel):
    created_date: datetime
    processed_date: datetime | None = None


class Storage(StorageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class StorageGetter(BaseModel):
    storage: Storage
    files: list[str] = list()


class FilePathRequest(BaseModel):
    file_name: str
