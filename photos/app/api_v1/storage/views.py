from fastapi import APIRouter, UploadFile, HTTPException, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.db import db
from .schemas.validators import _validate_files
from .schemas.models import StorageGetter, Storage, FilePathRequest
from .services import put_files_in_storage, get_files_from_storage, delete_stored_files, delete_stored_file
from .dals import StorageDAL
from .dependencies import get_storage_by_id

router = APIRouter(tags=['Storage'])


@router.get('/', response_model=list[Storage])
async def get_storages(session: AsyncSession = Depends(db.scoped_session_dependency)):
    return await StorageDAL(session).get_storages()


@router.post('/')
async def create_storage(
        request: Request,
        files: list[UploadFile],
        session: AsyncSession = Depends(db.scoped_session_dependency)
):
    validated_files = await _validate_files(files)
    storage = await StorageDAL(session).create_storage()

    return await put_files_in_storage(storage, validated_files, str(request.base_url))


@router.get('/{storage_id}/', response_model=StorageGetter)
async def get_storage(
        request: Request,
        storage=Depends(get_storage_by_id)
):
    result = {'storage': storage, 'files': await get_files_from_storage(storage, str(request.base_url))}
    return result


@router.post('/{storage_id}/', response_model=StorageGetter)
async def add_images_to_storage(
        request: Request,
        files: list[UploadFile],
        storage=Depends(get_storage_by_id),
):
    validated_files = await _validate_files(files)

    result = {'storage': storage, 'files': await put_files_in_storage(storage, validated_files, str(request.base_url))}
    return result


@router.delete('/{storage_id}')
async def delete_storage(
        storage=Depends(get_storage_by_id),
        session: AsyncSession = Depends(db.scoped_session_dependency)
) -> None:
    storage_id = storage.id

    await StorageDAL(session).delete_storage(storage)

    await delete_stored_files(storage_id)


@router.delete('/{storage_id}/delete/file')
async def delete_file_from_storage(
        request_data: FilePathRequest,
        storage=Depends(get_storage_by_id),
) -> None:
    await delete_stored_file(storage.id, request_data.file_name)
