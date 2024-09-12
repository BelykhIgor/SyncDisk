import configparser
from config import AUTH_TOKEN, BASE_URL

def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "BASE_URL", f"{BASE_URL}")
    config.set("Settings","OAuthToken", f"{AUTH_TOKEN}")

    with open(f"{path}/config.ini", "w") as config_file:
        config.write(config_file)
