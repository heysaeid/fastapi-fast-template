import os
from pathlib import Path
from argparse import ArgumentParser
from fastapi_fast_template.contents.database.database_dynamic_config import DatabaseDynamicConfig
from fastapi_fast_template.utils.enums import ConfigTypeEnum, DatabaseTypeEnum, FileEnum
from fastapi_fast_template.utils.helpers import get_app_config


class BaseContent:
    
    def __init__(self, args: ArgumentParser):
        self.app_config = get_app_config()
        self.config_type = self.app_config["config_type"] if self.app_config else args.config_type
        self.database_type = self.app_config["database_type"] if self.app_config else args.database_type
    
    def get_file_content(
        self, 
        file_path: str, 
        **kwargs
    ) -> str:        
        file = Path(f"{os.path.dirname(__file__)}/contents/{file_path}")
        file_content = file.read_text()
        
        content_data = {}
        for key, value in kwargs.items():
            if value is None:
                file_content = file_content.replace("{" + key + "}\n", "")
            else:
                content_data[key] = value
        
        if content_data:
            return file_content.format(**content_data)
        
        return file_content


class RootContent(BaseContent):
            
    def get_fast_template_ini(self) -> str:
        return """
[app]
config_type = {config_type}
database_type = {database_type}""".format(
        config_type = self.config_type, 
        database_type = self.database_type,
    )

    def get_gitignore(self) -> str:
        return self.get_file_content("git/.gitignore",)
    
    def get_env_sample(self) -> str:
        return self.get_file_content(
            "envs/.env.sample",
            db_env = DatabaseDynamicConfig.get_db_env_sample(self.database_type),
        )
        
    def get_conftest(self) -> str:
        return self.get_file_content("tests/conftest.py")
    
    
class SrcContent(BaseContent):
    
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
    
    def get_app(self) -> str:
        return self.get_file_content("main/app.py",)

    def get_main(self) -> str:
        return self.get_file_content("main/main.py",)
        
    def get_database(self) -> str:
        config_types = {
            DatabaseTypeEnum.SQLALCHEMY: "database/sqlalchemy.py",
        }
        return self.get_file_content(
            config_types[self.database_type],
        )
        
    def get_repository(self) -> str:
        repository = {
            DatabaseTypeEnum.SQLALCHEMY: "repositories/sqlalchemy/base.py",
        }
        return self.get_file_content(
            repository[self.database_type],
        )
        
    def get_lifespan(self) -> str:
        return self.get_file_content("utils/lifespan.py")
    
    def get_router_init(self) -> str:
        return self.get_file_content("routers/base.py")
    
    
class ExtensionContent(BaseContent):
    
    def get_babel_cfg(self) -> str:
        return "[python: **.py]"
    
    def get_babel_import_in_app(self) -> str:
        return "from fastapi_and_babel import FastAPIAndBabel"
    
    def get_babel_in_app(self, lang: str) -> str:
        return """
    translator = FastAPIAndBabel(__file__, app, "{lang}")""".format(lang=lang)
    
    def get_babel_in_fast_template_init(self) -> str:
        return "babel=True"
    
    def get_scheduler_in_fast_template_init(self) -> str:
        return "scheduler=True"
    
    def get_scheduler_init(self):
        return self.get_file_content("tasks/__init__.py")
    
    def get_scheduler_in_setting(self):
        return "\nenable_scheduler: bool = False"
    
    def get_scheduler_in_lifespan_import(self):
        return "from tasks import start_scheduler, shutdown_scheduler"
    
    def get_scheduler_in_lifespan_start_application(self):
        return "start_scheduler()"
    
    def get_scheduler_in_lifespan_down_application(self):
        return "shutdown_scheduler()"