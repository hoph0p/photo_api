from fastapi import UploadFile

from pydantic import BaseModel, validator

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


class FileValidator(BaseModel):
    file: UploadFile

    @validator("file")
    def validate_file(cls, file):
        ext = file.filename.split(".")[-1]
        if ext.lower() not in ALLOWED_EXTENSIONS:
            raise ValueError(f"Invalid file extension: {ext}. Allowed extensions: {ALLOWED_EXTENSIONS}")
        return file


async def _validate_files(files: list[UploadFile]) -> list:
    return [FileValidator(file=file).file for file in files]
