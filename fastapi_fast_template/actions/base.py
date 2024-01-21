from abc import ABC, abstractmethod
from argparse import _SubParsersAction, Namespace


class ActionABC(ABC):
    @abstractmethod
    def perform_action(self, args):
        pass


class ActionParserABC(ABC):
    def __init__(
        self, action_class: ActionABC, sub_parsers: _SubParsersAction
    ):
        self.action_class = action_class
        self.sub_parsers = sub_parsers

    @abstractmethod
    def parser(self, sub_parsers: _SubParsersAction):
        pass

    @abstractmethod
    def add_arguments(self, sub_parser):
        pass

    @abstractmethod
    def get_user_input(self, args: Namespace) -> None:
        ...

    def get_input(
        self,
        default_value: str,
        message: str,
        choices: list[str] = [],
    ):
        input_value = input(message)
        if input_value:
            if choices and input_value not in choices:
                print(
                    f"Invalid choice: {input_value} (choose from {', '.join(choices)})"
                )
                return self.__get_input(default_value, message, choices)
            return input_value
        return default_value
