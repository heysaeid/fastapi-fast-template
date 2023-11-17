import sys, os
from argparse import ArgumentParser
from fastapi_fast_template.actions.base import ActionABC, ActionParserABC
from fastapi_fast_template.content import ExtensionContent
from fastapi_fast_template.utils.enums import ExtensionNameEnum
from fastapi_fast_template.utils.helpers import add_new_line, FileBuilder, add_line_to_last_import



class ExtensionAction(ActionABC):

    def perform_action(self, args: ArgumentParser):
        if args.name == "babel":
            self.babel(args)

    def babel(self, args: ArgumentParser) -> None:
        ext_content = ExtensionContent(args)
        FileBuilder(file="./babel.cfg", build_function=ext_content.get_babel_cfg).build()
        os.system(f"pip install fastapi-and-babel")
        
        if not os.path.exists("./messages.pot"):
            os.system(f"pybabel extract -F babel.cfg -o messages.pot .")
        
        if not os.path.exists(f"./translations/{args.lang}"):
            os.system(f"pybabel init -i messages.pot -d translations -l {args.lang}")
            
        os.system(f"pybabel compile -d translations")
        add_line_to_last_import("src/app.py", ext_content.get_babel_import_in_app())
        add_new_line(
            file_path = "src/app.py", 
            search_value = "return app",
            new_line = ext_content.get_babel_in_app(lang = args.lang),
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