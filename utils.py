import os

from cryptography.fernet import Fernet

DEFAULT_KEY_FILE_NAME = "key.key"


def generate_key_and_save_to_file(filename=DEFAULT_KEY_FILE_NAME):
    # check key exist before generating
    if os.path.exists(filename):
        with open(filename, "rb") as key_file:
            _key = key_file.read()
        return _key

    _key = Fernet.generate_key()
    with open(filename, "wb") as key_file:
        key_file.write(_key)
    return _key


def get_key_from_file(filename=DEFAULT_KEY_FILE_NAME):
    if not os.path.exists(filename):
        raise Exception(f"{filename} file not found")

    with open(filename, "rb") as key_file:
        _key = key_file.read()
    return _key
