"""Главный модуль управления синхронизацией"""
from log.logging_init import logger

import schedule
from handlers.choose_cloud_dir import choose_dir, get_dir_info
from handlers.choose_local_dir import create_or_choose
import time
from handlers.synchronization import run_synchronization
from settings.config_init import start_config, set_config, get_url_auth_token
from handlers.crud import FileManager

BASE_URL, AUTH_TOKEN = get_url_auth_token()


def main():
    """
    Главная функция программы.

    В этой функции происходит:
    - Инициализация конфигурации и менеджера файлов.
    - Ввод данных от пользователя через главное меню:
       - Синхронизация локальной и облачной папок.
       - Получение списка файлов из облачного хранилища.
       - Получение списка папок на облачном диске.
       - Работа с корзиной: просмотр, восстановление, очистка.
       - Возможность выхода из программы.

    Если необходимые пути директорий не заданы в конфигурации,
    программа сообщает об этом и предлагает инициализировать конфигурацию.
    """
    config = start_config()
    file_manager = FileManager(BASE_URL, AUTH_TOKEN)

    if "local_dir" in config["Settings"] and "cloud_dir" in config["Settings"]:
        while True:
            query = input("Запустить программу синхронизации - 1\n"
                          "Получить список файлов из хранилища - 2\n"
                          "Получить список папок облачного диска - 3\n"
                          "Корзина - 4\n"
                          "Выход - exit\n"
                          "Введите соответствующее число >: ")
            print("--" * 20)

            if query == "1":
                """
                Запуск программы синхронизации.
                
                Пользователь запускает процесс синхронизации локальных файлов с облаком
                по указанным путям. Время синхронизации настраивается в конфигурации.
                """
                print("Старт программы, данные пути директорий установлены.")
                logger.info("Старт программы, данные пути директорий установлены.")
                print('Запускаем процесс синхронизации')
                print("--" * 20)
                time_sync = config.get("Settings", "time_sync")
                run_synchronization()
                schedule.every().day.at(time_sync).do(run_synchronization)

            elif query == "2":
                """
                Получение списка файлов из указанной папки облачного хранилища.
                
                Пользователь вводит название папки, и программа выводит список файлов,
                если такие файлы есть. Иначе сообщает, что файлов нет.
                """
                choose_dir = input("Введите название папки облачного диска: ")
                print("--" * 20)
                file_path = f"app:/{choose_dir}"
                cloud_files = file_manager.get_file_list(file_path)
                print(f"Список файлов директории - '{choose_dir}':")
                if cloud_files["_embedded"]["total"] != 0:
                    for folder in cloud_files["_embedded"]["items"]:
                        print(folder["name"])
                    print("--" * 20)
                else:
                    print(f"В папке '{choose_dir}' нет файлов\n")
                    print("--" * 20)

            elif query == "3":
                """
                Получение списка папок на облачном диске.
                
                Программа выводит список всех доступных папок на облачном диске.
                """
                folder_info = get_dir_info()
                folders = folder_info["_embedded"]["items"]
                for index, folder in enumerate(folders):
                    print(index + 1, folder["name"])
                print("--" * 20)

            elif query == "4":
                """
                Работа с корзиной.
                
                Пользователь может выбрать одну из следующих операций:
                - Просмотр списка файлов в корзине.
                - Восстановление файлов из корзины.
                - Очистка корзины.
                
                В зависимости от выбора, программа выполнит соответствующую операцию.
                """
                query_basket = input("Посмотреть файлы корзины - get\n"
                                     "Восстановить - restore\n"
                                     "Очистить корзину - del\n"
                                     "Введите соответствующую команду >: ")
                print("--" * 20)
                if query_basket == "get":
                    # Список файлов корзины.
                    print("Список файлов корзины:")
                    file_basket = file_manager.get_basket()
                    basket = file_basket["_embedded"]["items"]
                    for index, folder in enumerate(basket):
                        print(index + 1, folder["name"])
                    print("--" * 20)
                elif query_basket == "restore":
                    file_basket = file_manager.get_basket()
                    basket = file_basket["_embedded"]["items"]
                    for index, folder in enumerate(basket):
                        print(index + 1, folder["name"])
                    print("--" * 20)
                    file_restore = input("Введите номер файла, который нужно восстановить >: ")
                    for index, folder in enumerate(basket):
                        if index == int(file_restore) - 1:
                            print(folder["name"])
                            restore = file_manager.restore_file(folder["path"])
                            if restore == 201:
                                logger.info(f"Файл - '{folder['name']}' успешно восстановлен.")
                                print(f"Файл - {folder['name']} успешно восстановлен.\n")
                                print("--" * 20)
                            else:
                                logger.error(
                                    f"При восстановлении файла - {folder['name']} произошла ошибка. - {restore}")
                                print(f"При восстановлении файла - '{folder['name']}' произошла ошибка. - {restore}\n")
                                print("--" * 20)

                elif query_basket == "del":
                    response = file_manager.cleaning_trash()
                    if response == 202:
                        logger.info("Корзина успешно очищена!")
                        print("Корзина успешно очищена!")
                        print("--" * 20)
                    else:
                        logger.error(f"При очистке корзины возникли проблемы {response}")
                        print(f"При очистке корзины возникли проблемы {response}")
                        print("--" * 20)

            elif query.lower() == "exit":
                """
                Завершение программы.
                
                Программа завершит работу при вводе команды 'exit'.
                """
                print("Выход из программы...")
                break  # Прерывание цикла, завершение программы

            else:
                print("Неверный ввод, попробуйте снова.")
    else:
        logger.info("Старт программы, данные пути директорий не установлены.")
        print("Старт программы, данные пути директорий не установлены.")
        start_if_not_config_data()

def start_if_not_config_data():
    """
    Запуск программы синхронизации,
    когда пользователь еще не установил синхронизируемые директории.
    """
    print('Программа для синхронизации файлов между локальной папкой и папкой в облачном хранилище./n')
    input("Для запуска программы нажмите Enter.")
    print("--" * 20)
    print("Отлично, давайте выберем или создадим папку на вашем компьютере.")
    create_or_choose() # Функция создания или выбора папки для синхронизации на компьютере.
    print("--" * 20)
    print('Хорошо, теперь нужно выбрать или создать новую папку на облачном диске.')
    choose_dir() # Функция выбора или создания папки для синхронизации на облачном диске.
    print("--" * 20)
    print('Теперь нужно задать время синхронизации в формате ЧЧ:ММ.')
    time_sync = input("Введите время >: ")
    set_config("time_sync", f"{time_sync}")
    print("--" * 20)
    # Добавление в планировщик времени запуска программы синхронизации.
    schedule.every().day.at(time_sync).do(run_synchronization)

def start_scheduler():
    # Основной цикл, который проверяет и выполняет запланированные задачи
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
    start_scheduler()
