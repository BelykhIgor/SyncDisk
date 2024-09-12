import requests
from handlers.crud import FileManager
import os
from settings.config_init import get_config_data
from log.logging_init import logger
import time


def run_synchronization():
    """
        Выполняет синхронизацию файлов между локальной папкой и облачным хранилищем Яндекс.Диска.

        Основные шаги:
        1. Получает список файлов в локальной папке и их дату последней модификации.
        2. Запрашивает список файлов в указанной папке на Яндекс.Диске, включая их метаданные.
        3. Сравнивает списки файлов и определяет:
           - Какие файлы нужно загрузить на Яндекс.Диск (если файл есть в локальной папке, но отсутствует в облаке).
           - Какие файлы нужно удалить из облака (если файл есть в облаке, но отсутствует в локальной папке).
        4. Загрузка новых файлов на Яндекс.Диск с указанием времени создания в `custom_properties`.
        5. Удаление файлов из Яндекс.Диска, если они были удалены из локальной папки.

        Обработка ошибок:
        - В случае проблем с подключением к Яндекс.Диску выводится сообщение об ошибке и она логируется.
        - Логируются также ошибки, связанные с таймаутом и другими исключениями.

        Исключения:
            requests.ConnectionError: Если нет подключения к интернету или Яндекс.Диску.
            requests.Timeout: В случае превышения времени ожидания.
            Exception: Общие ошибки, возникающие во время выполнения запросов.

        Логирование:
        - Все ключевые события логируются с использованием системы логирования (например, информация о загрузке или удалении файлов).
    """
    local_path, cloud_path, base_url, auth_token = get_config_data()

    # Получаем список файлов в локальной папке.
    list_local_files = set()
    file_list = []
    for dirs, folder, files in os.walk(local_path):
        file_list = files

    for file in file_list:
        file_path = os.path.join(local_path, file)
        modification_time = os.path.getmtime(file_path)
        formatted_local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modification_time))
        list_local_files.add((file, formatted_local_time))
    print(f"Файлы в локальной папке:")
    for local_file in list_local_files:
        print(local_file[0])
    print("--" * 20)


    # Получаем список файлов в папке облачного хранилища.
    list_cloud_files = set()
    file_manager = FileManager(base_url, auth_token)
    try:
        cloud_files = file_manager.get_file_list(cloud_path)
        for folder in cloud_files["_embedded"]["items"]:
            if "custom_properties" in folder:
                time_created = folder["custom_properties"]["created"]
                list_cloud_files.add((folder["name"], time_created))
            else:
                list_cloud_files.add((folder["name"], ""))
        print(f"Файлы в облаке:")
        for cl_file in list_cloud_files:
            print(cl_file[0])
        print("--" * 20)
        # Выборка файлов для отправки на диск.
        files_for_send_cloud = list_local_files - list_cloud_files
        logger.info(f"Файлы для отправки в облако - {files_for_send_cloud}")
        print(f"Файлы для отправки в облако:")
        for send_file in files_for_send_cloud:
            print(send_file)
        print("--" * 20)
        for file_upload in files_for_send_cloud:
            custom_properties_data = {}
            file_data = file_upload
            path_to_upload = f"{cloud_path}/{file_data[0]}"
            # Получаем ссылку для загрузки файла.
            custom_properties_data['created'] = file_data[1]

            href = file_manager.get_upload_link(path_to_upload)
            if href:
                load_path = f"{local_path}/{file_data[0]}"
                # Отправляем файл на сервер.
                upload = file_manager.upload_file(href, load_path)
                if upload == 201:
                    logger.info(f"Загрузка файла {file_data[0]} успешно завершена")
                    print(f"Загрузка файла успешно завершена - {file_data[0]}")
                    print("--" * 20)
                else:
                    logger.error(f"Ошибка при загрузке файла {file_data[0]} - {upload}")
                    print(f"Ошибка при загрузке файла {file_data[0]} - {upload}")
                    print("--" * 20)
                file_manager.upload_timestamp_file(path_to_upload, custom_properties_data)

        # Выборка файлов для удаления с диска.
        files_from_delete = list_cloud_files - list_local_files
        logger.info(f"Файлы для удаления с диска - {files_from_delete}")
        print(f"Файлы для удаления с диска:")
        for file_delete in files_from_delete:
            print(file_delete[0])
        print("--" * 20)
        if files_from_delete:
            for file_delete in files_from_delete:
                file = file_delete
                path_to_delete = f"{cloud_path}/{file[0]}"
                response = file_manager.delete_file(path_to_delete)
                if response == 204:
                    logger.info(f"Удаление файла {file[0]} прошло успешно")
                    print(f"Удаление файла '{file[0]}' прошло успешно\n")
                    print("--" * 20)
                else:
                    logger.info(f"При удалении файла {file[0]} произошла ошибка, статус код - {response}")
                    print(f"При удалении файла {file[0]} произошла ошибка, статус код - {response}")
                    print("--" * 20)
    except requests.ConnectionError:
        logger.info("Ошибка подключения к Яндекс.Диску. Проверьте подключение к интернету.")
        print("Ошибка подключения к Яндекс.Диску. Проверьте подключение к интернету.")
    except requests.Timeout:
        logger.info("Превышено время ожидания для Яндекс.Диска.")
        print("Превышено время ожидания для Яндекс.Диска.")
    except Exception as e:
        logger.info(f"Произошла ошибка при запросе к Яндекс.Диску: {e}")
        print(f"Произошла ошибка при запросе к Яндекс.Диску: {e}")


if __name__ == '__main__':
    run_synchronization()
