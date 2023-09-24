from pathlib import Path

from fastapi import UploadFile, HTTPException, status

from ...db.models import Storage
from ...config import media_settings


async def get_storage_file_url(storage_id: id, file_name: str, base_url: str) -> str:
    return base_url + str(Path(media_settings.storage_url[1:], str(storage_id), file_name))


async def put_files_in_storage(storage: Storage, files: list[UploadFile], base_url: str) -> list[str]:
    directory = Path(media_settings.storage_root, str(storage.id))
    directory.mkdir(parents=True, exist_ok=True)

    file_urls = []

    for upload_file in files:
        file_path = Path(directory, upload_file.filename)
        with open(file_path, "wb") as file_obj:
            file_obj.write(await upload_file.read())
            file_urls.append(await get_storage_file_url(storage.id, Path(file_obj.name).name, base_url))

    return file_urls


async def get_files_from_storage(storage: Storage, base_url: str) -> list[str]:
    return [
        await get_storage_file_url(storage.id, f.name, base_url) for f in
        Path(media_settings.storage_root, str(storage.id)).iterdir()
    ]


async def delete_stored_files(storage_id) -> None:
    storage_path = Path(media_settings.storage_root, str(storage_id))
    for file_path in storage_path.iterdir():
        if file_path.is_file():
            file_path.unlink()
    storage_path.rmdir()


async def delete_stored_file(storage_id, file_path) -> None:
    file_path = Path(media_settings.storage_root, str(storage_id), file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No {file_path.name} in {storage_id} storage!'
        )
    file_path.unlink()
