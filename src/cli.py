import os
from typing import List
from content import BaseContent


class Action:
    
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
        }
        created_files = []
        for file in files:
            if not exist_ok or not os.path.exists(file):
                with open(file, 'w') as f:
                    file_action = files_with_action.get(file)
                    if file_action:
                        f.write(file_action())
                created_files.append(file)
            else:
                print(f"{file} already exists")
        if created_files:
            print(f"The following files were successfully created: {', '.join(created_files)}")

    
    @classmethod
    def init(cls) -> None:
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
        cls.create_dirs(dirs)
    
    
class Cli:
    
    def main() -> None:
        pass