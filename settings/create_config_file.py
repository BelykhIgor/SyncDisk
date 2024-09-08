import configparser
from config import AUTH_TOKEN, BASE_URL

def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "ClientID", "8f1d356f24b74b168b0ec6a333490adb")
    config.set("Settings", "Client_secret", "d209e1ee2d154a64bd6ba500b454aad7")
    config.set("Settings", "BASE_URL", f"{BASE_URL}")
    config.set("Settings","OAuthToken", f"{AUTH_TOKEN}")

    with open(f"{path}/config.ini", "w") as config_file:
        config.write(config_file)

