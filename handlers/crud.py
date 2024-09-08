import requests
import urllib.parse



class FileManager:
    """
    Класс для взаимодействия с Яндекс.Диском через REST API.

    Атрибуты:
        BASE_URL (str): Базовый URL для работы с API.
        AUTH_TOKEN (str): Токен для аутентификации.
        headers (dict): Заголовки HTTP-запросов.

    Методы:
        encode_path(path): Кодирует путь в формат URL.
        get_folder_info(folder_path): Получает информацию о содержимом папки.
        get_upload_link(load_path): Получает ссылку для загрузки файла.
        upload_file(href, local_path): Загружает файл на Яндекс.Диск.
        create_folder(path): Создает новую папку на Яндекс.Диске.
        get_file_list(path): Получает список файлов в указанной папке.
        delete_file(file_path): Удаляет файл на Яндекс.Диске.
        get_basket(): Получает содержимое корзины.
        restore_file(path): Восстанавливает файл из корзины.
        cleaning_trash(): Очищает корзину.
    """

    def __init__(self, BASE_URL, AUTH_TOKEN):
        self.BASE_URL = BASE_URL
        self.AUTH_TOKEN = AUTH_TOKEN
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'OAuth {AUTH_TOKEN}',
        }

    def encode_path(self, path):
        """
        Кодирует путь для URL.

        :param path: Строка пути.
        :return: Закодированный путь.
        """
        return urllib.parse.quote(path)

    def get_folder_info(self, folder_path):
        """
        Получает информацию о содержимом указанной папки.

        :param folder_path: Путь к папке.
        :return: Содержимое папки в виде JSON.
        """
        try:
            response = requests.get(f"{self.BASE_URL}?path={folder_path}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при получении информации о папке: {e}")
            return None

    def get_upload_link(self, load_path):
        """
        Получает ссылку для загрузки файла.

        :param load_path: Путь на Яндекс.Диске.
        :return: URL для загрузки файла.
        """
        try:
            encoded_path = self.encode_path(load_path)
            response = requests.get(
                f"{self.BASE_URL}/upload?path={encoded_path}&overwrite=true",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get("href")
        except requests.RequestException as e:
            print(f"Ошибка при получении ссылки для загрузки: {e}")
            return None

    def upload_file(self, href, local_path):
        """
        Загружает файл на Яндекс.Диск.

        :param href: Ссылка для загрузки файла.
        :param local_path: Локальный путь к файлу.
        :return: Код статуса HTTP.
        """
        try:
            with open(local_path, 'rb') as file:
                response = requests.post(href, files={'file': file})
                response.raise_for_status()
                return response.status_code
        except (requests.RequestException, IOError) as e:
            print(f"Ошибка при загрузке файла: {e}")
            return None

    def create_folder(self, path):
        """
        Создает новую папку на Яндекс.Диске.

        :param path: Путь для новой папки.
        :return: Ответ API в виде JSON.
        """
        try:
            response = requests.put(f"{self.BASE_URL}?path={path}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при создании папки: {e}")
            return None

    def get_file_list(self, path):
        """
        Получает список файлов в указанной папке.

        :param path: Путь к папке.
        :return: Список файлов в виде JSON.
        """
        try:
            encoded_path = self.encode_path(path)
            response = requests.get(f"{self.BASE_URL}?path={encoded_path}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при получении списка файлов: {e}")
            return None

    def delete_file(self, file_path):
        """
        Удаляет файл на Яндекс.Диске.

        :param file_path: Путь к файлу.
        :return: Код статуса HTTP.
        """
        try:
            encoded_path = self.encode_path(file_path)
            response = requests.delete(f"{self.BASE_URL}?path={encoded_path}", headers=self.headers)
            response.raise_for_status()
            return response.status_code
        except requests.RequestException as e:
            print(f"Ошибка при удалении файла: {e}")
            return None

    def get_basket(self):
        """
        Получает содержимое корзины.

        :return: Список файлов в корзине в виде JSON.
        """
        try:
            response = requests.get("https://cloud-api.yandex.net/v1/disk/trash/resources", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при получении содержимого корзины: {e}")
            return None

    def restore_file(self, path):
        """
        Восстанавливает файл из корзины.

        :param path: Путь к файлу в корзине.
        :return: Код статуса HTTP.
        """
        try:
            restore_url = "https://cloud-api.yandex.net/v1/disk/trash/resources/restore"
            encoded_path = self.encode_path(path)
            response = requests.put(f"{restore_url}?path={encoded_path}", headers=self.headers)
            response.raise_for_status()
            return response.status_code
        except requests.RequestException as e:
            print(f"Ошибка при восстановлении файла: {e}")
            return None

    def cleaning_trash(self):
        """
        Очищает корзину.

        :return: Код статуса HTTP.
        """
        try:
            response = requests.delete("https://cloud-api.yandex.net/v1/disk/trash/resources", headers=self.headers)
            response.raise_for_status()
            return response.status_code
        except requests.RequestException as e:
            print(f"Ошибка при очистке корзины: {e}")
            return None