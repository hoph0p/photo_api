from pathlib import Path

from fastapi import UploadFile

from ...db.models import Storage
from ...config import media_settings


async def get_image_url(storage_id: id, file_name: str) -> str:
    return str(Path(media_settings.media_ulr, str(storage_id), file_name))


async def put_files_in_storage(storage: Storage, files: list[UploadFile]) -> list[str]:
    directory = Path(media_settings.storage_root, str(storage.id))
    directory.mkdir(parents=True, exist_ok=True)

    filenames = []

    for upload_file in files:
        file_path = Path(directory, upload_file.filename)
        with open(file_path, "wb") as file_obj:
            file_obj.write(await upload_file.read())
            filenames.append(await get_image_url(storage.id, Path(file_obj.name).name))

    return filenames


async def get_files_from_storage(storage: Storage) -> list[str]:
    return [
        await get_image_url(storage.id, f.name) for f in Path(media_settings.storage_root, str(storage.id)).iterdir()
    ]
