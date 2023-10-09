from fastapi import APIRouter, UploadFile, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.db import db
from .schemas.validators import _validate_files
from .schemas.models import StorageGetter, Storage, FilePathRequest
from .services.manager import StorageDirectoryManager
from .dals import StorageDAL
from .dependencies import get_storage_by_id

router = APIRouter(tags=['Storage'])


@router.get('/', response_model=list[Storage])
async def get_storages(session: AsyncSession = Depends(db.scoped_session_dependency)):
    result = await StorageDAL(session).get_storages()
    if not result:
        raise HTTPException(status_code=404, detail='No storages fow now')
    return result


@router.post('/', response_model=StorageGetter)
async def create_storage(
        request: Request,
        files: list[UploadFile],
        session: AsyncSession = Depends(db.scoped_session_dependency)
):
    validated_files = await _validate_files(files)
    storage = await StorageDAL(session).create_storage()

    result = {
        'storage': storage,
        'files': await StorageDirectoryManager(storage.id, str(request.base_url)).put_files(validated_files)
    }
    return result


@router.get('/{storage_id}/', response_model=StorageGetter)
async def get_storage(
        request: Request,
        storage=Depends(get_storage_by_id)
):
    result = {
        'storage': storage,
        'files': await StorageDirectoryManager(storage.id, str(request.base_url)).get_files_url()
    }
    return result


@router.post('/{storage_id}/', response_model=StorageGetter)
async def add_images_to_storage(
        request: Request,
        files: list[UploadFile],
        storage=Depends(get_storage_by_id),
):
    validated_files = await _validate_files(files)

    result = {
        'storage': storage,
        'files': await StorageDirectoryManager(storage.id, str(request.base_url)).put_files(validated_files)
    }
    return result


@router.delete('/{storage_id}')
async def delete_storage(
        storage=Depends(get_storage_by_id),
        session: AsyncSession = Depends(db.scoped_session_dependency)
) -> None:
    storage_id = storage.id

    await StorageDAL(session).delete_storage(storage)

    await StorageDirectoryManager(storage_id).delete_storage()


@router.delete('/{storage_id}/delete/file')
async def delete_file_from_storage(
        request_data: FilePathRequest,
        storage=Depends(get_storage_by_id),
) -> None:
    await StorageDirectoryManager(storage.id).delete_file(request_data.file_name)
