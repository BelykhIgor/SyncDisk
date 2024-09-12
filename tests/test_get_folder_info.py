import pytest
from handlers.crud import FileManager

from unittest.mock import patch

BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
AUTH_TOKEN = "fake_token"


# Проверка получения информации об базовом диске приложения.
def test_base_url_request():
    file_manager = FileManager(BASE_URL, AUTH_TOKEN)

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "href": "https://example.com",
            "method": "GET",
            "templated": False
        }

        # Выполняем запрос для проверки доступности BASE_URL
        response = file_manager.get_folder_info("app:/")

        # Проверяем, что запрос был выполнен один раз и был успешным
        mock_get.assert_called_once_with(f"{BASE_URL}?path=app:/", headers=file_manager.headers)

        # Проверяем статус ответа и структуру возвращаемого json
        assert response["href"] == "https://example.com"
        assert response["method"] == "GET"
        assert response["templated"] == False
