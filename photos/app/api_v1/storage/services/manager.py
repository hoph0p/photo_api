from pathlib import Path

from fastapi import UploadFile, HTTPException, status

from config import media_settings


class StorageDirectoryManager:
    """Class for managing storage directory in media directory"""

    def __init__(self, storage_id: int, base_url: str = None):
        self.storage_path = Path(media_settings.storage_root, str(storage_id))
        self.base_url = base_url
        print(self.storage_path)

    async def get_files_name(self) -> list[str]:
        return [f.name for f in self.storage_path.iterdir()]

    async def get_file_url(self, file_name: str) -> str:
        return self.base_url + str(Path(media_settings.storage_url[1:], self.storage_path.name, file_name))

    async def get_files_url(self) -> list[str]:
        return [await self.get_file_url(file_name) for file_name in await self.get_files_name()]

    async def put_files(self, files: list[UploadFile]) -> list[str]:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        for upload_file in files:
            file_path = Path(self.storage_path, upload_file.filename)
            with open(file_path, 'wb') as file_obj:
                file_obj.write(await upload_file.read())

        return await self.get_files_url()

    async def delete_file(self, file_name) -> None:
        file_path = Path(self.storage_path, file_name)
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'No {file_name} in {self.storage_path.name} storage!'
            )
        file_path.unlink()

    async def delete_storage(self) -> None:
        for file_path in self.storage_path.iterdir():
            if file_path.is_file():
                file_path.unlink()
        self.storage_path.rmdir()
