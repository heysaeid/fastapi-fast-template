import os
from pathlib import Path
from src.contents.database.database_dynamic_config import DatabaseDynamicConfig
from src.utils.enums import ConfigTypeEnum, DatabaseTypeEnum


class Content:
    
    def __init__(
        self, 
        config_type: ConfigTypeEnum,
        database_type: DatabaseTypeEnum,
    ):
        self.config_type = config_type
        self.database_type = database_type 
    
    def get_file_content(
        self, 
        file_path: str, 
        **kwargs
    ) -> str:
        file = Path(os.path.abspath(f"../src/contents/{file_path}"))
        file_content = file.read_text()
        
        content_data = {}
        for key, value in kwargs.items():
            if value is None:
                file_content = file_content.replace("{" + key + "}\n", "")
            else:
                content_data[key] = value
        
        return file_content.format(**content_data)

    def get_config(self, app_name: str) -> str:
        config_types = {
            ConfigTypeEnum.MULTIPLE: "configs/config.py",
            ConfigTypeEnum.SINGLE: "configs/single_config.py"
        }
        return self.get_file_content(
            config_types[self.config_type], 
            app_name = app_name, 
            db_config = DatabaseDynamicConfig.get_db_config(self.database_type),
        )

    def get_gitignore(self) -> str:
        return self.get_file_content("git/.gitignore",)

    def get_app(self) -> str:
        return self.get_file_content("main/app.py",)

    def get_main(self) -> str:
        return self.get_file_content("main/main.py",)
        
    def get_env_sample(self) -> str:
        return self.get_file_content(
            "envs/.env.sample",
            db_env = DatabaseDynamicConfig.get_db_env_sample(self.database_type),
        )
        
    def get_database(self) -> str:
        config_types = {
            DatabaseTypeEnum.SQLALCHEMY: "database/sqlalchemy.py",
        }
        return self.get_file_content(
            config_types[self.database_type],
        )