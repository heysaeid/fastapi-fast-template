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

def find_line_in_file(value, file_path):
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if value in line:
                return line_number, line.strip()
    return None

def add_new_line(file_path, search_value, new_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if search_value in line:
                file.write(new_line + '\n')
            file.write(line)


def add_line_to_last_import(file_path, new_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    last_import_index = -1
    for i, line in enumerate(lines):
        if line.startswith("from") and "import" in line:
            last_import_index = i

    if last_import_index != -1:
        lines.insert(last_import_index + 1, new_line + '\n')

    with open(file_path, 'w') as file:
        file.writelines(lines)


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
