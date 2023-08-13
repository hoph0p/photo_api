import os
import datetime
import settings
from typing import List
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRouter
from pydantic import BaseModel, validator

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


class Storage(Base):
    """Photo storage indexing model"""
    __tablename__ = 'storage'

    id = Column(Integer, primary_key=True, index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    processed_date = Column(DateTime, nullable=True)


class StorageDAL:
    """Data Access Layer for interacting with storage"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_storage(self) -> Storage:
        new_storage = Storage()
        self.db_session.add(new_storage)
        await self.db_session.flush()
        return new_storage


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


class FileValidator(BaseModel):
    file: UploadFile

    @validator("file")
    def validate_file(cls, file):
        ext = file.filename.split(".")[-1]
        if ext.lower() not in ALLOWED_EXTENSIONS:
            raise ValueError(f"Invalid file extension: {ext}. Allowed extensions: {ALLOWED_EXTENSIONS}")
        return file


app = FastAPI(
    title="Photo Processor"
)
storage_router = APIRouter()
storage_directory = os.path.join(settings.MEDIA_ROOT, 'storage')
app.mount("/storage", StaticFiles(directory=storage_directory), name="storage")


async def _validate_files(files: List[UploadFile]) -> List:
    return [FileValidator(file=file).file for file in files]


async def _create_storage() -> Storage:
    async with async_session() as session:
        async with session.begin():
            storage_dal = StorageDAL(session)
            storage = await storage_dal.create_storage()
            return storage


async def _put_files_in_storage(storage: Storage, files: List[UploadFile]) -> List[str]:
    directory = os.path.join(storage_directory, str(storage.id))
    os.makedirs(directory, exist_ok=True)

    filenames = []

    for upload_file in files:
        file_path = os.path.join(directory, upload_file.filename)
        with open(file_path, "wb") as file_obj:
            file_obj.write(await upload_file.read())
            filenames.append(file_obj.name)

    return filenames


@storage_router.post("/create/")
async def create_storage(files: List[UploadFile]):
    validated_files = await _validate_files(files)
    storage = await _create_storage()

    return await _put_files_in_storage(storage, validated_files)


main_api_router = APIRouter()
main_api_router.include_router(storage_router, prefix='/storage', tags=['storage'])
app.include_router(main_api_router, prefix='/api')
