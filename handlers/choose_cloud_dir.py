from handlers.crud import FileManager
from settings.config_init import set_config, get_url_auth_token
from log.logging_init import logger

BASE_URL, AUTH_TOKEN = get_url_auth_token()


def get_dir_info():
    """
    Получение информации о директориях и файлах в облачном хранилище Яндекс.Диск.

    :return: Информация о папках и файлах (dict), либо None в случае ошибки.
    """
    dir_path = "app:/"
    file_manager = FileManager(BASE_URL, AUTH_TOKEN)
    try:
        folder_info = file_manager.get_folder_info(dir_path)
        return folder_info
    except Exception as e:
        logger.error(f"Ошибка получения информации о директориях: {e}")
        print(f"Ошибка получения информации о директориях: {e}")
        return None


def choose_dir():
    """
    Позволяет пользователю выбрать папку из облачного хранилища или создать новую папку.

    Обрабатывает выбор папки из списка существующих, создание новой папки в облаке,
    а также настройку конфигурации с выбранным путем.
    """
    try:
        query = input("Выбрать папку из списка - 1\n"
                      "Создать новую папку в облачном хранилище - 2\n"
                      "Введите соответствующее число >: ")

        if query == "1":
            folder_info = get_dir_info()
            if folder_info:
                print("Список файлов и папок облачного диска:")
                folders = folder_info["_embedded"]["items"]
                for index, folder in enumerate(folders):
                    print(index + 1, folder["name"])

                try:
                    query_dir = input("Введите число для выбора директории >: ")
                    dir_name = "app:/" + folders[int(query_dir) - 1]["name"]
                    logger.info(f"Выбрана директория в облачном хранилище - {dir_name}")
                    set_config(option="cloud_dir", value=dir_name)
                    print(f"Выбрана директория: {dir_name}")
                except (ValueError, IndexError) as e:
                    logger.error(f"Некорректный ввод при выборе директории: {e}")
                    print("Некорректный ввод. Пожалуйста, введите правильное число.")
            else:
                print("В облачном диске отсутствуют файлы и папки.")
                query = input("Создать новую папку в облачном хранилище - 2")

        if query == "2":
            print("Создаем новую папку в облачном хранилище.")
            new_folder_name = input("Введите наименование папки: ")
            file_manager = FileManager(BASE_URL, AUTH_TOKEN)
            dir_path = f"app:/{new_folder_name}"
            encoded_path = file_manager.encode_path(dir_path)

            try:
                create_folder = file_manager.create_folder(encoded_path)
                if create_folder:
                    logger.info(f"Создана директория в облаке - {dir_path}")
                    print(f"Директория `{new_folder_name}` успешно создана\n")
                    set_config(option="cloud_dir", value=dir_path)
                else:
                    logger.error("Произошла ошибка создания новой директории")
                    print("Произошла ошибка создания новой директории")
            except Exception as e:
                logger.error(f"Ошибка при создании директории: {e}")
                print(f"Ошибка при создании директории: {e}")

    except Exception as e:
        logger.error(f"Ошибка выполнения операции: {e}")
        print(f"Произошла ошибка: {e}")


if __name__ == '__main__':
    choose_dir()