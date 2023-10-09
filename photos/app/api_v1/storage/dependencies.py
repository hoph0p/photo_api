from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .dals import StorageDAL
from db.models.db import db
from db.models import Storage


async def get_storage_by_id(
        storage_id: Annotated[int, Path],
        session: AsyncSession = Depends(db.scoped_session_dependency)
) -> Storage:
    storage = await StorageDAL(session).get_storage(storage_id)

    if not storage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Storage {storage_id} not found!'
        )

    return storage
