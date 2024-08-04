from argparse import Namespace

from termcolor import colored

from fastapi_fast_template.actions.base import ActionABC, ActionParserABC


class DocAction(ActionABC):
    url_color = "blue"

    def perform_action(self, args):
        self.get_extension_doc()

    def get_title(self, title: str):
        print(f"\t{title}")

    def get_extension_doc(self):
        print(
            colored(
                "\n\tQuick access to the documents of the tools used in this template.",
                color="green",
            )
        )
        print("\t___________________________________\n")
        print(
            f"\t👉 FastAPI                            {self.get_url('https://fastapi.tiangolo.com')}"
        )
        print(
            f"\t👉 SQLAlchemy                         {self.get_url('https://www.sqlalchemy.org')}"
        )
        print(
            f"\t👉 Tortoise ORM                       {self.get_url('https://tortoise.github.io')}"
        )
        print(
            f"\t👉 SQLModel ORM                       {self.get_url('https://sqlmodel.tiangolo.com/')}"
        )
        print(
            f"\t👉 Beanie ODM                         {self.get_url('https://beanie-odm.dev')}"
        )
        print(
            f"\t👉 FastAPI-And-Babel                  {self.get_url('https://github.com/heysaeid/fastapi-and-babel')}"
        )
        print(
            f"\t👉 FastAPI-And-Logging                {self.get_url('https://github.com/heysaeid/fastapi-and-logging')}"
        )
        print(
            f"\t👉 FastAPI-And-Caching                {self.get_url('https://github.com/heysaeid/fastapi-and-caching')}"
        )
        print(
            f"\t👉 APScheduler                        {self.get_url('https://fastapi.tiangolo.com')}"
        )
        print(
            f"\t👉 FastStream                         {self.get_url('https://faststream.airt.ai')}"
        )
        print("\t___________________________________\n")

    def get_url(self, url: str) -> str:
        return colored(url, "blue")


class DocActionParser(ActionParserABC):
    def parser(self):
        init = self.sub_parsers.add_parser(
            "doc", help="Add extension to the project."
        )
        self.add_arguments(init)
        init.set_defaults(func=self.action_class.perform_action)

    def add_arguments(self, sub_parser):
        pass

    def get_user_input(self, args: Namespace) -> None:
        raise NotImplementedError
