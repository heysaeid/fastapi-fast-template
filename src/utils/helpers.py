import os
import configparser


def get_app_config() -> dict:
    config = configparser.ConfigParser()
    project_root = os.getcwd()
    config.read(f'{project_root}/.fast_template.ini')
    return config