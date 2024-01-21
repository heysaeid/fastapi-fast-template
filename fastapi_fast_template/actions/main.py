import sys
from argparse import ArgumentParser
from fastapi_fast_template.actions.base import ActionABC, ActionParserABC
from fastapi_fast_template.content import RootContent, SrcContent
from fastapi_fast_template.utils.enums import (
    ActionEnum,
    ArgumentDefaultValueEnum,
    ConfigTypeEnum,
    DatabaseTypeEnum,
    DirectoryEnum,
    FileEnum,
)
from fastapi_fast_template.utils.helpers import create_directory, FileBuilder


class InitAction(ActionABC):
    def perform_action(self, args: ArgumentParser):
        action = sys.argv[-1]
        if action == ActionEnum.init:
            self.init(args)

    def init(self, args: ArgumentParser) -> None:
        self.create_initial_dirs()
        self.create_initial_files(args)
        print("Initializing has been done successfully.")

    def create_initial_dirs(self) -> None:
        directories = (
            DirectoryEnum.logs,
            DirectoryEnum.tests,
            DirectoryEnum.src,
            DirectoryEnum.src_routers,
            DirectoryEnum.src_repositories,
            DirectoryEnum.src_services,
            DirectoryEnum.src_models,
            DirectoryEnum.src_schemas,
            DirectoryEnum.src_utils,
        )
        created_dirs = []
        for directory in directories:
            is_created = create_directory(directory)
            if is_created:
                created_dirs.append(directory)
            else:
                print(f"{dir} already exists")
        if created_dirs:
            print(
                f"The following directories were successfully created: {', '.join(created_dirs)}"
            )

    def create_initial_files(self, args: ArgumentParser) -> None:
        self.root_content = RootContent(args)
        self.src_content = SrcContent(args)
        initial_files = [
            # root
            FileBuilder(
                file=".fast_template.ini",
                build_function=self.root_content.get_fast_template_ini,
            ),
            FileBuilder(
                file=".gitignore",
                build_function=self.root_content.get_gitignore,
            ),
            FileBuilder(
                file=".env.sample",
                build_function=self.root_content.get_env_sample,
            ),
            FileBuilder(file=".env"),
            # tests
            FileBuilder(file="tests/conftest.py"),
            # src
            FileBuilder(
                file=FileEnum.src_config,
                build_function=self.src_content.get_config,
                inputs={"app_name": args.app_name},
            ),
            FileBuilder(
                file=FileEnum.src_app, build_function=self.src_content.get_app
            ),
            FileBuilder(
                file=FileEnum.src_main,
                build_function=self.src_content.get_main,
            ),
            FileBuilder(
                file=FileEnum.src_database,
                build_function=self.src_content.get_database,
            ),
            FileBuilder(
                file=FileEnum.src_repo_base,
                build_function=self.src_content.get_repository,
            ),
            FileBuilder(
                file=FileEnum.src_routers_init_,
                build_function=self.src_content.get_router_init,
            ),
            FileBuilder(
                file=FileEnum.src_utils_lifespan,
                build_function=self.src_content.get_lifespan,
            ),
        ]
        for file in initial_files:
            file.build()
            print(f"File {file.file} has been created successfully.")


class InitActionParser(ActionParserABC):
    def parser(self):
        init = self.sub_parsers.add_parser(
            "init", help="Initialize your project."
        )
        self.add_arguments(init)
        init.set_defaults(func=self.action_class.perform_action)

    def add_arguments(self, sub_parser):
        sub_parser.add_argument(
            "-an",
            "--app_name",
            default=ArgumentDefaultValueEnum.APP_NAME,
            help="Application Name",
        )
        sub_parser.add_argument(
            "-ct",
            "--config_type",
            default=ArgumentDefaultValueEnum.CONFIG_TYPE,
            choices=ConfigTypeEnum.get_values(),
            help="Type config module",
        )
        sub_parser.add_argument(
            "-dbt",
            "--database_type",
            default=ArgumentDefaultValueEnum.DATABASE_TYPE,
            choices=DatabaseTypeEnum.get_values(),
            help="Database Type",
        )

    def get_user_input(self, args):
        args.app_name = self.get_input(
            default_value=args.app_name.value,
            message=f"Enter the name of the application (default: {ArgumentDefaultValueEnum.APP_NAME}): ",
        )
        args.config_type = self.get_input(
            default_value=args.config_type.value,
            message=f"Enter the config module type (default: {ArgumentDefaultValueEnum.CONFIG_TYPE}): ",
            choices=ConfigTypeEnum.get_values(),
        )
        args.database_type = self.get_input(
            default_value=args.database_type.value,
            message=f"Enter the database type (default: {ArgumentDefaultValueEnum.DATABASE_TYPE}): ",
            choices=DatabaseTypeEnum.get_values(),
        )
