import pprint
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PIL import Image
from fastapi import UploadFile

from api_v1.storage.services.manager import StorageDirectoryManager
from config import media_settings

pytest_plugins = ('pytest_asyncio',)


@pytest.fixture(autouse=True)
def mock_media_settings(monkeypatch):
    """
    Mocking media settings
    """

    media_root = Path('tests/media')
    media_url = '/test/media'

    storage_url = media_url + '/storage'
    storage_root = Path(media_root, 'storage')

    monkeypatch.setattr(media_settings, 'media_root', media_root)
    monkeypatch.setattr(media_settings, 'media_url', media_url)
    monkeypatch.setattr(media_settings, 'storage_url', storage_url)
    monkeypatch.setattr(media_settings, 'storage_root', storage_root)


@pytest.fixture(autouse=True)
def make_file():
    """
    Making test storage and file
    """

    image = Image.new(mode="RGB", size=(400, 400), color=(209, 123, 193))
    storage_path = Path('tests/media/storage/1/')
    storage_path.mkdir(parents=True, exist_ok=True)
    for i in range(3):
        image.save(str(storage_path) + f"/test_image_{i}.png")


@pytest.fixture
def storage_manager(mock_media_settings):
    return StorageDirectoryManager(storage_id=1, base_url="http://example.com/")


@pytest.fixture
def mocked_upload_files():
    upload_files = []
    for i in range(3, 6):
        file_name = f'test_image_{i}.png'
        upload_file_mock = MagicMock(spec=UploadFile)
        upload_file_mock.filename = file_name
        upload_file_mock.read.return_value = f"Content of {file_name}".encode("utf-8")
        upload_files.append(upload_file_mock)

    return upload_files


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'expected_files', [
        (
                ['test_image_0.png', 'test_image_1.png', 'test_image_2.png']
        )
    ]
)
async def test_get_files_name(storage_manager, expected_files):
    files = await storage_manager.get_files_name()
    assert sorted(files) == sorted(expected_files)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'expected_files_urls', [
        (
                [
                    'http://example.com/test/media/storage/1/test_image_0.png',
                    'http://example.com/test/media/storage/1/test_image_1.png',
                    'http://example.com/test/media/storage/1/test_image_2.png'
                ]
        )
    ]
)
async def test_get_files_url(storage_manager, expected_files_urls):
    files_urls = await storage_manager.get_files_url()
    assert sorted(files_urls) == sorted(expected_files_urls)


@pytest.mark.asyncio
async def test_put_files(storage_manager, mocked_upload_files):
    urls = await storage_manager.put_files(mocked_upload_files)
    assert sorted(urls) == sorted([
        'http://example.com/test/media/storage/1/test_image_0.png',
        'http://example.com/test/media/storage/1/test_image_1.png',
        'http://example.com/test/media/storage/1/test_image_2.png',
        'http://example.com/test/media/storage/1/test_image_3.png',
        'http://example.com/test/media/storage/1/test_image_4.png',
        'http://example.com/test/media/storage/1/test_image_5.png'
    ])

    # Assert the files were written
    for file in mocked_upload_files:
        expected_file_path = storage_manager.storage_path / file.filename
        assert expected_file_path.is_file()

        # Clean up - delete the created files after the test
        expected_file_path.unlink()


@pytest.mark.asyncio
@pytest.mark.parametrize('file_name', ['test_image_2.png'])
async def test_delete_file(storage_manager, file_name):
    await storage_manager.delete_file(file_name)

    assert Path(storage_manager.storage_path, file_name).is_file() is False


@pytest.mark.asyncio
async def test_delete_storage(storage_manager):
    await storage_manager.delete_storage()
    print(storage_manager)
    assert storage_manager.storage_path.exists() is False