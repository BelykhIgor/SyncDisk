from settings.config_init import set_config, start_config


def test_create_config():
    # Записываем в файл конфигурации тестовые данные.
    option = "Test Option"
    value = "Test Value"
    set_config(option, value)

    # Проверяем соответствие.
    config = start_config()
    config_data = config.get("Settings", option)
    assert config_data == value
    # Удаляем тестовую запись из файла конфигурации.
    config.remove_option("Settings", option)



