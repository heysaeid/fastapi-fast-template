import os
import sys
import argparse
from src.content import (
    get_app, 
    get_config, 
    get_env_sample, 
    get_gitignore, 
    get_main,
)
from src.utils.enums import ArgumentDefaultValueEnum, ConfigTypeEnum


class Action:
    
    @staticmethod
    def create_dirs(directories: list[str]) -> None:
        """
        Create directories if they don't exist.

        Args:
            directories (List[str]): A list of directory paths to create.

        Returns:
            None

        Examples:
            >>> create_dirs(['dir1', 'dir2', 'dir3'])
            The following directories were successfully created: dir1, dir2, dir3

        """
        created_dirs = []
        
        for dir in directories:
            if not os.path.exists(dir):
                os.makedirs(dir)
                created_dirs.append(dir)
            else:
                print(f"{dir} already exists")
                
        if created_dirs:
            print(f"The following directories were successfully created: {', '.join(created_dirs)}")
    
    @staticmethod
    def create_files(files: list[str], exist_ok: bool = True) -> None:
        """
        Create files if they don't exist.

        Args:
            files (list[str]): A list of file paths to create.
            exist_ok (bool): A flag indicating whether to check if the file already exists before creating it.
                Defaults to True.

        Returns:
            None

        Examples:
            >>> create_files(['./src/config.py', './src/main.py', './.gitignore'])
            The following files were successfully created: ./src/config.py, ./src/main.py, ./.gitignore

        """
        files_with_action = {
            "./.gitignore": get_gitignore,
            ".env.sample": get_env_sample,
            "src/config.py": get_config,
            "src/app.py": get_app,
            "src/main.py": get_main,
        }
        created_files = []
        for file in files:
            file_name = file.pop("file")
            if not exist_ok or not os.path.exists(file_name):
                with open(file_name, 'w') as f:
                    file_action = files_with_action.get(file_name)
                    if file_action:
                        f.write(file_action(**file))
                    else:
                        f.write("")
                created_files.append(file_name)
            else:
                print(f"{file_name} already exists")
        if created_files:
            print(f"The following files were successfully created: {', '.join(created_files)}")

    @classmethod
    def init(cls, args) -> None:
        dirs = (
            "./logs",
            "./tests",
            "./src",
            "./src/controllers",
            "./src/repositories",
            "./src/services",
            "./src/models",
            "./src/schemas",
        )
        files = (
            {"file": ".gitignore"},
            {"file": ".env.sample"},
            {"file": ".env"},
            {"file": "src/config.py", "type": args.config_type, "app_name": args.app_name},
            {"file": "src/app.py"},
            {"file": "src/main.py"},
        )
        cls.create_dirs(dirs)
        cls.create_files(files)
        
        action = sys.argv[-1]
        if action == "init":
            print("Initializing has been done successfully.")
    
    
class Cli:
    
    @classmethod
    def main(cls) -> None:
        parser = argparse.ArgumentParser(
            prog='fast', 
            description='FastAPI Fast Template CLI'
        )
        sub_parsers = parser.add_subparsers()
        
        init = sub_parsers.add_parser('init', help="Initialize your project.")
        init.add_argument(
            "-an", 
            "--app_name", 
            default = ArgumentDefaultValueEnum.APP_NAME,
            help = "Application Name",
        )
        init.add_argument(
            "-ct", 
            "--config_type", 
            default = ArgumentDefaultValueEnum.CONFIG_TYPE,
            choices = ConfigTypeEnum.get_values(),
            help="Type config module",
        )
        init.set_defaults(func=Action.init)
        args = parser.parse_args()

        args.app_name = cls.get_input(
            default_value = args.app_name.value,
            message = f"Enter the name of the application (default: {ArgumentDefaultValueEnum.APP_NAME}): ",
        )
        args.config_type = cls.get_input(
            default_value = args.config_type.value,
            message = f"Enter the config module type (default: {ArgumentDefaultValueEnum.CONFIG_TYPE}): ",
            choices = ConfigTypeEnum.get_values(),
        )
        
        args.func(args)
    
    @classmethod 
    def get_input(
        cls,
        default_value: str, 
        message: str, 
        choices: list[str] = [],
    ):
        input_value = input(message)
        if input_value:
            if choices and input_value not in choices:
                print(f"Invalid choice: {input_value} (choose from {', '.join(choices)})")
                return cls.get_input(default_value, message, choices)
            return input_value
        return default_value