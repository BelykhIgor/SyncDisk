import os
from settings.config_init import set_config
from log.logging_init import logger


# Проверка существования пути.
def check_path(path):
    """
    Проверяет, существует ли указанный путь.

    :param path: Путь к директории или файлу.
    :return: Путь, если существует, или None.
    """
    if os.path.exists(path):
        return path
    else:
        return None


# Проверка, что данной папки еще нет в директории.
def find_file(dir_name, starting_directory):
    """
    Ищет папку с указанным именем, начиная с заданной директории.

    :param dir_name: Имя папки для поиска.
    :param starting_directory: Директория, с которой начинается поиск.
    :return: Полный путь к папке, если она найдена, иначе None.
    """
    for root, dirs, files in os.walk(starting_directory):
        if dir_name in dirs:
            path = os.path.join(root, dir_name)
            return path
    return None


# Сбор данных, путь, название папки или путь к уже созданной папке.
def create_or_choose():
    """
    Позволяет пользователю создать новую папку или выбрать существующую для синхронизации.

    Пользователь может выбрать:
    - Создать новую папку по указанному пути.
    - Выбрать уже существующую папку.

    :return: True, если папка успешно выбрана или создана.
    """
    while True:
        query = input(
            "Создать новую папку - 1\n"
            "Выбрать свою - 2\n"
            "Введите соответствующее число: "
        )
        if query == "1":
            while True:
                choice_disk = input(
                    "Укажите путь для создания новой папки\n"
                    "Например:\n"
                    "C:/Users/<имя пользователя>/Documents\n"
                    "или C:/\n"
                    ">: "
                )
                encoded_path = choice_disk.replace('\\', '/').lstrip('\\')
                check_path_dir = check_path(encoded_path)

                if check_path_dir:
                    while True:
                        dir_name = input("Введите название папки: ")
                        if os.path.exists(f"{check_path_dir}/{dir_name}"):
                            print(f"Папка с таким именем {dir_name} уже существует.")
                            logger.error(f"Папка с таким именем {dir_name} уже существует.")
                        else:
                            try:
                                full_path = os.path.join(encoded_path, dir_name)
                                os.makedirs(full_path)
                                logger.info(f"Папка {dir_name} успешно создана по пути {full_path}")
                                print(f"Папка {dir_name} успешно создана по пути {full_path}.")
                                set_config(option="local_dir", value=full_path)
                                return True
                            except OSError as e:
                                logger.error(f"Ошибка при создании папки {dir_name}: {e}")
                                print(f"Ошибка при создании папки: {e}")
                else:
                    print("Ошибка ввода. Пожалуйста, введите корректный путь.")
        elif query == "2":
            choice_disk = input("Укажите путь к вашей папке\n>: ")
            encoded_path = choice_disk.replace('\\', '/').lstrip('\\')
            check_path_dir = check_path(encoded_path)
            if check_path_dir and os.path.exists(check_path_dir):
                set_config(option="local_dir", value=check_path_dir)
                print(f"Вы выбрали папку: {check_path_dir}")
                logger.info(f"Локальная папка для синхронизации - {check_path_dir}")
                return True
            else:
                logger.error(f"Ошибка ввода. {check_path_dir} путь не найден.")
                print("Ошибка ввода. Путь не найден.")
        else:
            print("Неправильный ввод. Попробуйте снова.")


if __name__ == '__main__':
    path = create_or_choose()