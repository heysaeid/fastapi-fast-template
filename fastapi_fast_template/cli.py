import argparse
import sys

from fastapi_fast_template.actions.doc import DocAction, DocActionParser
from fastapi_fast_template.actions.extension import (
    ExtensionAction,
    ExtensionActionParser,
)
from fastapi_fast_template.actions.main import InitAction, InitActionParser
from fastapi_fast_template.utils.enums import ActionEnum


class Cli:
    def __init__(self, sub_parsers: argparse._SubParsersAction) -> None:
        self.sub_parsers = sub_parsers
        self.init_action_parser = InitActionParser(
            action_class=InitAction(),
            sub_parsers=self.sub_parsers,
        )
        self.extension_action_parser = ExtensionActionParser(
            action_class=ExtensionAction(),
            sub_parsers=self.sub_parsers,
        )
        self.doc_action_parser = DocActionParser(
            action_class=DocAction(),
            sub_parsers=self.sub_parsers,
        )

    @classmethod
    def main(cls) -> None:
        parser = argparse.ArgumentParser(
            prog="fast",
            description="FastAPI Fast Template CLI",
        )
        sub_parsers = parser.add_subparsers()
        instance = cls(sub_parsers)
        instance.init_action_parser.parser()
        instance.extension_action_parser.parser()
        instance.doc_action_parser.parser()
        instance.__parse_args(parser)

    def __parse_args(self, parser: argparse.ArgumentParser) -> None:
        args = parser.parse_args()

        action = sys.argv[1]
        if action == ActionEnum.INIT:
            self.init_action_parser.get_user_input(args)
        elif action == ActionEnum.EXTENSION:
            self.extension_action_parser.get_user_input(args)

        args.func(args)
