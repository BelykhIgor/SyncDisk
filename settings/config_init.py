import configparser
import os
from log.logging_init import logger
from settings.create_config_file import createConfig


current_file_path  = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)

def start_config() -> configparser.ConfigParser:
    """Функция создает при отсутствии файл config.ini и инициализирует configparser"""
    logger.info("Start configparser.")
    config_path = os.path.join(current_directory, "config.ini")

    if not os.path.exists(config_path):
        createConfig(current_directory)

    config = configparser.ConfigParser()

    with open(config_path, "r", encoding="utf-8") as config_file:
        config.read_file(config_file)
    return config

def get_url_auth_token() -> [str, str]:
    """Функция для получения из файла настроек базового url и токена аутентификации"""
    logger.info("Start function to get BASE_URL and AUTH_TOKEN.")
    config = start_config()
    BASE_URL = config.get("Settings", "base_url")
    AUTH_TOKEN = config.get("Settings", "oauthtoken")
    return BASE_URL, AUTH_TOKEN

def get_config_data():
    config = start_config()
    local_path = config.get("Settings", "local_dir")
    cloud_path = config.get("Settings", "cloud_dir")
    base_url = config.get("Settings", "base_url")
    auth_token = config.get("Settings", "oauthtoken")
    return local_path, cloud_path, base_url, auth_token

def set_config(option, value):
    """Функция добавления в файл конфигурации новых данных."""
    logger.info("Add in config.ini option and value.")
    config = start_config()
    config.set("Settings", option, value)

    with open(os.path.join(current_directory, "config.ini"), "w", encoding="utf-8") as config_file:
        config.write(config_file)


if __name__ == '__main__':
    get_url_auth_token()