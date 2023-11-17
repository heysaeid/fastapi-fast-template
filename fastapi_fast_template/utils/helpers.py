import os
from dataclasses import dataclass
from configparser import ConfigParser


def create_directory(directory: str) -> bool:
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    return False

def create_file(
    file: str,
    file_content: str = "",
    exist_ok: bool = True,
) -> None:
    if not exist_ok or not os.path.exists(file):
        with open(file, 'w') as f:
            f.write(file_content)
        return True
    return False

def get_app_config() -> dict | None:
    config = ConfigParser()
    project_root = os.getcwd()
    config.read(f'{project_root}/.fast_template.ini')
    if "app" in config:
        return config["app"]
    return


class FileBuilder:
    
    def __init__(self, file: str, build_function: callable = None, inputs: dict = {}):
        self.file = file
        self.build_function = build_function
        self.inputs = inputs
    
    def build(self) -> bool:
        return create_file(
            file=self.file, 
            file_content=self.build_function(**self.inputs) if self.build_function else "",
        )
