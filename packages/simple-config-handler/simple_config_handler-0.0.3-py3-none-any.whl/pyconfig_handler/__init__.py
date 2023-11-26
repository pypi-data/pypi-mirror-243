import os
import sys
import json

_USER_CONFIG = None
USER_CONFIG_DIR = None
CONFIG_DIR = None
_BASE_CONFIG = None
PLATFORM = None
CONFIG_FILE = None
USER_CONFIG_FILE = None
BASE_CONFIG_FILE = None


def init(progname: str, base_config: dict = None):
    """
    Initialize the pyconfig_handler module.
    :param progname: (STR): Name used to identify the program
    :param base_config: (DICT): default for the config
    :return: None
    """
    global _BASE_CONFIG
    global USER_CONFIG_DIR
    global CONFIG_DIR
    global _BASE_CONFIG
    global PLATFORM
    global CONFIG_FILE
    global BASE_CONFIG_FILE
    if sys.platform.startswith("win"):
        PLATFORM = "windows"
        CONFIG_DIR = os.path.join(os.path.expanduser("~"), "APPDATA", "local", progname)
    elif sys.platform == "darwin":
        PLATFORM = "macos"
        CONFIG_DIR = os.path.join(os.path.expanduser("~"), "Library", "Application Support", progname)
    elif sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "cygwin":
        PLATFORM = "linux"
        CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", progname)
    else:
        raise NotImplementedError(f"Unsupported platform: {sys.platform}")
    CONFIG_FILE = os.path.join(CONFIG_DIR)
    USER_CONFIG_DIR = os.path.join(CONFIG_DIR, "user-config")
    BASE_CONFIG_FILE = os.path.join(CONFIG_DIR, "base-config.json")
    _BASE_CONFIG = base_config
    if not os.path.exists(USER_CONFIG_DIR):
        os.makedirs(USER_CONFIG_DIR)
    BASE_CONFIG_FILE = os.path.join(CONFIG_DIR, "base-config.json")
    if base_config is not None:
        _BASE_CONFIG = base_config
    else:
        _BASE_CONFIG = {}
    if not os.path.exists(BASE_CONFIG_FILE):
        with open(BASE_CONFIG_FILE, "w") as f:
            json.dump(base_config, f)


def load_base_config():
    """
    Load the base configuration.
    :return: (DICT) The base configuration
    """
    global _BASE_CONFIG
    global BASE_CONFIG_FILE
    with open(BASE_CONFIG_FILE, "r") as f:
        _BASE_CONFIG = json.load(f)
    return _BASE_CONFIG


def load_user_config(user: str, default_data: dict = None):
    """
    Load the user configuration.
    :param user: (STR): name to identify the user
    :param default_data: (DICT): default configuration
    :return: (DICT) The user configuration
    """
    global _USER_CONFIG
    global USER_CONFIG_FILE
    USER_CONFIG_FILE = os.path.join(USER_CONFIG_DIR, f"{user}-config.json")
    if default_data is None:
        default_data = {}
    if not os.path.exists(USER_CONFIG_FILE):
        with open(USER_CONFIG_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_CONFIG_FILE, "r") as f:
        _USER_CONFIG = json.load(f)
    if user not in _USER_CONFIG:
        _USER_CONFIG[user] = default_data
        with open(USER_CONFIG_FILE, "w") as f:
            json.dump(_USER_CONFIG, f)
    return _USER_CONFIG[user]


def update_base_config(data: dict = None):
    """
    Update the base configuration with the provided data.
    :param data: (DICT): The new base configuration
    :return: None
    """
    global _BASE_CONFIG
    global BASE_CONFIG_FILE
    if data is None:
        data = {}
    _BASE_CONFIG = data
    with open(BASE_CONFIG_FILE, "w") as f:
        json.dump(data, f)


def get_config(which: str = "base"):
    """
    Get the configuration.
    :param which: (STR): base or user
    :return: (DICT) The configuration
    """
    global _BASE_CONFIG
    global _USER_CONFIG
    if which == "base":
        return _BASE_CONFIG
    elif which == "user":
        return _USER_CONFIG


def update_user_config(data: dict = None):
    """
    Update the user configuration with the provided data.

    Args:
        data (dict): The new user configuration data.

    Returns:
        None
    """
    global _USER_CONFIG
    global USER_CONFIG_FILE

    if data is None:
        data = {}

    _USER_CONFIG = data

    with open(USER_CONFIG_FILE, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    raise NotImplementedError
