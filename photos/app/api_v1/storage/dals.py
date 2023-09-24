from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.models import Storage


class StorageDAL:
    """Data Access Layer for interacting with storage"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_storage(self) -> Storage:
        new_storage = Storage()
        self.db_session.add(new_storage)
        await self.db_session.commit()
        return new_storage

    async def get_storages(self) -> list[Storage]:
        stmt = select(Storage).order_by(Storage.id)
        result: Result = await self.db_session.execute(stmt)
        storages = result.scalars().all()
        return list(storages)

    async def get_storage(self, storage_id: int) -> Storage | None:
        return await self.db_session.get(Storage, storage_id)
