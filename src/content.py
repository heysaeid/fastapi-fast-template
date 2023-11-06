import os
from pathlib import Path
from src.utils.enums import ConfigTypeEnum


def get_file_content(file_path: str, **kwargs) -> str:
    file = Path(os.path.abspath(f"../src/contents/{file_path}"))
    return (file.read_text()).format(**kwargs)

def get_config(type: ConfigTypeEnum, app_name: str) -> str:
    config_type = {
        ConfigTypeEnum.MULTIPLE: "configs/config.py",
        ConfigTypeEnum.SINGLE: "configs/single_config.py"
    }
    return get_file_content(config_type[type], app_name = app_name)

def get_gitignore() -> str:
    return get_file_content("git/.gitignore",)

def get_app() -> str:
    return get_file_content("main/app.py",)

def get_main() -> str:
    return get_file_content("main/main.py",)
    
def get_env_sample() -> str:
    return get_file_content("envs/.env.sample",)