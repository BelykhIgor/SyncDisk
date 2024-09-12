import pytest
import requests
from handlers.crud import FileManager
from settings.config_init import get_url_auth_token
from urllib.parse import urlparse


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

BASE_URL, AUTH_TOKEN = get_url_auth_token()

@pytest.fixture
def file_manager():
    base_url = BASE_URL
    auth_token = AUTH_TOKEN
    return FileManager(base_url, auth_token)


@pytest.mark.parametrize("url", ["https://cloud-api.yandex.net"])
def test_get(url):
    response = requests.get(url)
    assert response.status_code == 200

# Тест получения детальной информации о папке в облаке.
def test_get_folder_info():
    file_manager = FileManager(BASE_URL, AUTH_TOKEN)
    dir_name = "Image"
    error_dir_name = "TestDir"
    response = file_manager.get_folder_info(f"app:/{dir_name}")

    assert isinstance(response, dict)
    assert response["name"] == dir_name
    assert response["name"] != error_dir_name

# Тест на получение списка директорий удаленного диска.
def test_get_folder_list():
    file_manager = FileManager(BASE_URL, AUTH_TOKEN)
    response = file_manager.get_folder_info(f"app:/")

    assert isinstance(response, dict)
    assert isinstance(response["_embedded"]["items"], list)
    for dir_name in response["_embedded"]["items"]:
        assert isinstance(dir_name["name"], str)

# Тест на создание/удаление папки на удаленном диске.
def test_create_dir_cloud():
    file_manager = FileManager(BASE_URL, AUTH_TOKEN)
    disk_path = "app:/"
    folder_name = "TestFolder"

    # Создаем новую папку.
    response_create = file_manager.create_folder(f"{disk_path}{folder_name}")
    response_data = response_create.json()
    response_status_code = response_create.status_code
    assert response_status_code == 201
    assert isinstance(response_data["href"], str)
    assert response_data["method"] == "GET"
    assert response_data["templated"] == False

    # Удаляем созданную папку.
    response_delete = file_manager.delete_file(f"{disk_path}{folder_name}")
    assert response_delete == 204


# Тест на загрузку файла, получение информации о файле, удаление файла.
def test_upload_and_delete_file():
    file_manager = FileManager(BASE_URL, AUTH_TOKEN)
    cloud_disk = "app:/"
    file_path = "file_for_pytest.txt"
    # Получаем ссылку для загрузки файла.
    upload_link = file_manager.get_upload_link(f"{cloud_disk}{file_path}")
    assert is_valid_url(upload_link) == True, f"{upload_link} is not a valid URL"

    # Отправляем файл на диск.
    upload_file = file_manager.upload_file(upload_link, file_path)

