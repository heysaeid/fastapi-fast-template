import os
import sys
from typing import List
import argparse
from content import BaseContent


class Action:
    
    @staticmethod
    def create_dirs(directories: List[str]) -> None:
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
    def create_files(files: List[str], exist_ok: bool = True) -> None:
        """
        Create files if they don't exist.

        Args:
            files (List[str]): A list of file paths to create.
            exist_ok (bool, optional): A flag indicating whether to check if the file already exists before creating it.
                Defaults to True.

        Returns:
            None

        Examples:
            >>> create_files(['./src/config.py', './src/main.py', './.gitignore'])
            The following files were successfully created: ./src/config.py, ./src/main.py, ./.gitignore

        """
        files_with_action = {
            "./.gitignore": BaseContent.get_gitignore,
            ".env.sample": BaseContent.get_env_sample,
            "src/config.py": BaseContent.get_config,
            "src/app.py": BaseContent.get_app,
            "src/main.py": BaseContent.get_main,
        }
        created_files = []
        for file in files:
            if not exist_ok or not os.path.exists(file):
                with open(file, 'w') as f:
                    file_action = files_with_action.get(file)
                    if file_action:
                        f.write(file_action())
                    else:
                        f.write("")
                created_files.append(file)
            else:
                print(f"{file} already exists")
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
            "./.gitignore",
            "./.env.sample"
            "./.env",
            "src/config.py",
            "src/app.py",
            "src/main.py",
        )
        cls.create_dirs(dirs)
        cls.create_files(files)
        
        action = sys.argv[-1]
        if action == "init":
            print("Initializing has been done successfully.")
    
    
class Cli:
    
    @staticmethod
    def main() -> None:
        parser = argparse.ArgumentParser(
            prog='fastapi', 
            description='FastAPI Fast Template CLI'
        )
        sub_parsers = parser.add_subparsers()
        
        init = sub_parsers.add_parser('init', help="Initialize your project.")
        init.set_defaults(func=Action.init)
        
        args = parser.parse_args()
        args.func(args)