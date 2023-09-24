from fastapi import APIRouter, UploadFile, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.db import db
from .schemas.validators import _validate_files
from .schemas.models import StorageGetter
from .services import put_files_in_storage, get_files_from_storage
from .dals import StorageDAL

router = APIRouter(tags=['Storage'])


@router.post("/")
async def create_storage(
        files: list[UploadFile],
        session: AsyncSession = Depends(db.scoped_session_dependency)
):
    validated_files = await _validate_files(files)
    storage = await StorageDAL(session).create_storage()

    return await put_files_in_storage(storage, validated_files)


@router.get('/{storage_id}/', response_model=StorageGetter)
async def get_storage(
        storage_id: int,
        session: AsyncSession = Depends(db.scoped_session_dependency)
):
    storage = await StorageDAL(session).get_storage(storage_id)

    if not storage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Storage {storage_id} not found!'
        )
    result = {'storage': storage, 'files': await get_files_from_storage(storage)}
    return result
