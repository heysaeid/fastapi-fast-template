import os
from argparse import ArgumentParser
from fastapi_fast_template.actions.base import ActionABC, ActionParserABC
from fastapi_fast_template.content import ExtensionContent
from fastapi_fast_template.utils.enums import (
    DirectoryEnum, 
    ExtensionNameEnum, 
    FileEnum,
)
from fastapi_fast_template.utils.helpers import (
    FileBuilder,
    add_new_line, 
    add_line_to_last_import,
    add_text_to_obj_end,
    check_extension_exists,
    create_directory,
)


class ExtensionAction(ActionABC):

    def perform_action(self, args: ArgumentParser):
        if args.name == ExtensionNameEnum.babel:
            self.babel(args)
        elif args.name == ExtensionNameEnum.scheduler:
            self.scheduler(args)

    def babel(self, args: ArgumentParser) -> None:
        ext_content = ExtensionContent(args)
        FileBuilder(file="./babel.cfg", build_function=ext_content.get_babel_cfg).build()
        os.system(f"pip install fastapi-and-babel")
        
        if not os.path.exists("./messages.pot"):
            os.system(f"pybabel extract -F babel.cfg -o messages.pot .")
        
        if not os.path.exists(f"./translations/{args.lang}"):
            os.system(f"pybabel init -i messages.pot -d translations -l {args.lang}")
            
        os.system(f"pybabel compile -d translations")
        add_line_to_last_import(FileEnum.src_app, ext_content.get_babel_import_in_app())
        add_new_line(
            file_path = FileEnum.src_app, 
            search_value = "return app",
            new_line = ext_content.get_babel_in_app(lang = args.lang),
        )
        add_new_line(
            file_path = FileEnum.fast_template_init, 
            search_value = "babel",
            remove_matched = True,
            new_line = ext_content.get_babel_in_fast_template_init(),
        )
        
    def scheduler(self, args: ArgumentParser) -> None:
        if check_extension_exists(ExtensionNameEnum.scheduler):
            print("You have already added the scheduler")
            return 
        
        ext_content = ExtensionContent(args)
        create_directory(DirectoryEnum.src_tasks)
        FileBuilder(file=FileEnum.src_tasks_init_, build_function=ext_content.get_scheduler_init).build()
        add_new_line(
            file_path = FileEnum.fast_template_init, 
            search_value = "scheduler",
            remove_matched = True,
            new_line = ext_content.get_scheduler_in_fast_template_init(),
        )
        add_text_to_obj_end(
            file_path = FileEnum.src_config,
            class_name = "Settings",
            text_to_add = ext_content.get_scheduler_in_setting()
        )
        add_line_to_last_import(
            FileEnum.src_utils_lifespan,
            new_line = ext_content.get_scheduler_in_lifespan_import(),
        )
        add_text_to_obj_end(
            FileEnum.src_utils_lifespan,
            async_function_name = "start_application",
            text_to_add = ext_content.get_scheduler_in_lifespan_start_application(),
        )
        add_text_to_obj_end(
            FileEnum.src_utils_lifespan,
            async_function_name = "down_application",
            text_to_add = ext_content.get_scheduler_in_lifespan_down_application(),
        )

class ExtensionActionParser(ActionParserABC):
    
    def parser(self):
        init = self.sub_parsers.add_parser('extension', help="Add extension to the project.")
        self.add_arguments(init)
        init.set_defaults(func=self.action_class.perform_action)
        
    def add_arguments(self, sub_parser):
        sub_parser.add_argument(
            "-n", 
            "--name", 
            help = "Extension Name",
        )
        sub_parser.add_argument(
            "-lg",
            "--lang", 
            default = "en",
            help = "Language Name",
        )
        
    def get_user_input(self, args):
        if args.name == ExtensionNameEnum.babel:
            args.lang = self.get_input(
                default_value = args.lang,
                message = f"Please select the default language (default: en): ",
            )