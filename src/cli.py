import os
from typing import List


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
    
    def create_files(files: List[str], check_exists_file: bool = True) -> None:
        pass
    
    def init() -> None:
        pass
    
    
class Cli:
    
    def main() -> None:
        pass