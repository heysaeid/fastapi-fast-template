import sys
import argparse
from fastapi_fast_template.actions.main import InitAction, InitActionParser
from fastapi_fast_template.content import RootContent, SrcContent
from fastapi_fast_template.utils.enums import ActionEnum


class Cli:
    
    def __init__(self, sub_parsers: argparse._SubParsersAction) -> None:
        self.sub_parsers = sub_parsers
        self.init_action_parser = InitActionParser(
            action_class=InitAction(), 
            sub_parsers=self.sub_parsers,
        )
    
    @classmethod
    def main(cls) -> None:
        parser = argparse.ArgumentParser(
            prog='fast', 
            description='FastAPI Fast Template CLI',
        )
        sub_parsers = parser.add_subparsers()
        instance = cls(sub_parsers)
        instance.init_action_parser.parser()
        instance.__parse_args(parser)
        
    def __parse_args(self, parser: argparse.ArgumentParser) -> None:
        args = parser.parse_args()

        action = sys.argv[-1]
        if action == ActionEnum.init:
            self.init_action_parser.get_user_input(args)
        
        args.func(args)