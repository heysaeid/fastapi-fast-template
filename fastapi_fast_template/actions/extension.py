import os
from argparse import ArgumentParser

from fastapi_fast_template.actions.base import ActionABC, ActionParserABC
from fastapi_fast_template.content import ExtensionContent
from fastapi_fast_template.utils.enums import (
    ArgumentDefaultValueEnum,
    AuthEnum,
    CachingBackendEnum,
    DirectoryEnum,
    ExtensionNameEnum,
    FileEnum,
    LoggingTypeEnum,
    StreamBrokerEnum,
)
from fastapi_fast_template.utils.helpers import (
    FileBuilder,
    add_line_to_last_import,
    add_new_line,
    add_text_to_obj_end,
    check_extension_exists,
    create_directory,
)


class ExtensionAction(ActionABC):
    def perform_action(self, args: ArgumentParser):
        if args.name == ExtensionNameEnum.BABEL:
            self.babel(args)
        elif args.name == ExtensionNameEnum.SCHEDULER:
            self.scheduler(args)
        elif args.name == ExtensionNameEnum.CACHING:
            self.caching(args)
        elif args.name == ExtensionNameEnum.LOGGING:
            self.logging(args)
        elif args.name == ExtensionNameEnum.STREAM:
            self.stream(args)
        elif args.name == ExtensionNameEnum.AUTH:
            self.auth(args)

    def babel(self, args: ArgumentParser) -> None:
        os.system("pip install fastapi-and-babel")

        ext_content = ExtensionContent(args)
        FileBuilder(
            file="./babel.cfg", build_function=ext_content.get_babel_cfg
        ).build()

        if not os.path.exists("./messages.pot"):
            os.system("pybabel extract -F babel.cfg -o messages.pot .")

        if not os.path.exists(f"./translations/{args.lang}"):
            os.system(
                f"pybabel init -i messages.pot -d translations -l {args.lang}"
            )

        os.system("pybabel compile -d translations")
        add_line_to_last_import(
            FileEnum.SRC_APP, ext_content.get_babel_import_in_app()
        )
        add_new_line(
            file_path=FileEnum.SRC_APP,
            search_value="return app",
            new_line=ext_content.get_babel_in_app(lang=args.lang),
        )
        add_new_line(
            file_path=FileEnum.FAST_TEMPLATE_INIT,
            search_value="babel",
            remove_matched=True,
            new_line=ext_content.get_babel_in_fast_template_init(),
        )

    def scheduler(self, args: ArgumentParser) -> None:
        if check_extension_exists(ExtensionNameEnum.SCHEDULER):
            print("You have already added the scheduler")
            return

        os.system("pip install APScheduler")
        ext_content = ExtensionContent(args)

        create_directory(DirectoryEnum.SRC_TASKS)
        FileBuilder(
            file=FileEnum.SRC_TASKS_INIT_,
            build_function=ext_content.get_scheduler_init,
        ).build()
        add_new_line(
            file_path=FileEnum.FAST_TEMPLATE_INIT,
            search_value="scheduler",
            remove_matched=True,
            new_line=ext_content.get_scheduler_in_fast_template_init(),
        )
        add_text_to_obj_end(
            file_path=FileEnum.SRC_CONFIG,
            class_name="Settings",
            text_to_add=ext_content.get_scheduler_in_setting(),
        )
        add_line_to_last_import(
            FileEnum.SRC_UTILS_LIFESPAN,
            new_line=ext_content.get_scheduler_in_lifespan_import(),
        )
        add_text_to_obj_end(
            FileEnum.SRC_UTILS_LIFESPAN,
            async_function_name="start_application",
            text_to_add=ext_content.get_scheduler_in_lifespan_start_application(),
        )
        add_text_to_obj_end(
            FileEnum.SRC_UTILS_LIFESPAN,
            async_function_name="down_application",
            text_to_add=ext_content.get_scheduler_in_lifespan_down_application(),
        )

    def caching(self, args: ArgumentParser) -> None:
        if check_extension_exists(ExtensionNameEnum.CACHING):
            print("You have already added the caching")
            return

        os.system("pip install fastapi-and-caching")
        ext_content = ExtensionContent(args)

        FileBuilder(
            file=FileEnum.SRC_UTILS_CACHING,
            build_function=ext_content.get_caching_in_caching,
        ).build()
        add_new_line(
            file_path=FileEnum.FAST_TEMPLATE_INIT,
            search_value="caching",
            remove_matched=True,
            new_line=ext_content.get_caching_in_fast_template_init(),
        )
        add_text_to_obj_end(
            file_path=FileEnum.SRC_CONFIG,
            class_name="Settings",
            text_to_add=ext_content.get_caching_in_setting(),
        )
        add_line_to_last_import(
            FileEnum.SRC_UTILS_LIFESPAN,
            new_line=ext_content.get_caching_in_lifespan_import(),
        )
        add_text_to_obj_end(
            FileEnum.SRC_UTILS_LIFESPAN,
            async_function_name="start_application",
            text_to_add=ext_content.get_caching_in_lifespan_start_application(),
        )
        add_text_to_obj_end(
            FileEnum.SRC_UTILS_LIFESPAN,
            async_function_name="down_application",
            text_to_add=ext_content.get_caching_in_lifespan_down_application(),
        )

    def logging(self, args: ArgumentParser) -> None:
        if check_extension_exists(f"{args.logging_type}_log"):
            print(f"You have already added the {args.logging_type}")
            return

        os.system("pip install fastapi-and-logging")
        ext_content = ExtensionContent(args)

        add_new_line(
            file_path=FileEnum.FAST_TEMPLATE_INIT,
            search_value="caching",
            remove_matched=True,
            new_line=ext_content.get_logging_in_fast_template_init(
                type=args.logging_type,
            ),
        )
        add_new_line(
            file_path=FileEnum.SRC_APP,
            search_value="return app",
            new_line=ext_content.get_logging_class_in_app(
                type=args.logging_type,
            ),
        )
        add_line_to_last_import(
            FileEnum.SRC_APP,
            new_line=ext_content.get_logging_import_in_app(
                type=args.logging_type,
            ),
        )

    def stream(self, args: ArgumentParser) -> None:
        if check_extension_exists(ExtensionNameEnum.STREAM):
            print(f"You have already added the {args.broker}")
            return

        stream_brokers = {
            StreamBrokerEnum.AIOKAFKA: "kafka",
            StreamBrokerEnum.CONFLUENT: "kafka",
            StreamBrokerEnum.REDIS: "redis",
            StreamBrokerEnum.RABBIT: "rabbit",
            StreamBrokerEnum.NATS: "nats",
        }
        os.system(f"pip install faststream[{stream_brokers[args.broker]}]")

        ext_content = ExtensionContent(args)
        FileBuilder(
            file=FileEnum.SRC_STREAM,
            build_function=ext_content.get_stream_in_stream,
        ).build()
        add_new_line(
            file_path=FileEnum.FAST_TEMPLATE_INIT,
            search_value="stream",
            remove_matched=True,
            new_line=ext_content.get_stream_in_fast_template_init(),
        )
        add_text_to_obj_end(
            file_path=FileEnum.SRC_CONFIG,
            class_name="Settings",
            text_to_add=ext_content.get_stream_in_config(),
        )
        add_new_line(
            file_path=FileEnum.SRC_UTILS_LIFESPAN,
            new_line=ext_content.get_stream_in_lifespan(),
        )

    def auth(self, args: ArgumentParser):
        os.system("pip install authx")
        if check_extension_exists(ExtensionNameEnum.AUTH):
            print(f"You have already added the {args.auth}")
            return
        ext_content = ExtensionContent(args)
        FileBuilder(
            file=FileEnum.SRC_UTILS_AUTHX,
            build_function=ext_content.get_scheduler_init,
        ).build()
        add_line_to_last_import(
            FileEnum.FileEnum.SRC_APP,
            new_line=ext_content.get_authx_import_in_app(),
        )
        add_new_line(
            file_path=FileEnum.SRC_APP,
            search_value="return",
            new_line=ext_content.get_authx_in_app(),
        )


class ExtensionActionParser(ActionParserABC):
    def parser(self):
        init = self.sub_parsers.add_parser(
            "extension", help="Add extension to the project."
        )
        self.add_arguments(init)
        init.set_defaults(func=self.action_class.perform_action)

    def add_arguments(self, sub_parser):
        sub_parser.add_argument(
            "-n",
            "--name",
            help="Extension Name",
        )
        sub_parser.add_argument(
            "-lg",
            "--lang",
            default="en",
            help="Language Name",
        )
        sub_parser.add_argument(
            "-b",
            "--backend",
            default=ArgumentDefaultValueEnum.REDIS_BACKEND,
            help="Backend Name",
        )
        sub_parser.add_argument(
            "-lt",
            "--logging_type",
            default=ArgumentDefaultValueEnum.LOGGING_TYPE,
            help="Type Name",
        )
        sub_parser.add_argument(
            "-sb",
            "--broker",
            default=ArgumentDefaultValueEnum.STREAM_BROKER,
            help="Broker Name",
        )
        sub_parser.add_argument(
            "-ath",
            "--auth",
            default=ArgumentDefaultValueEnum.AUTH,
            help="Auth-Ext Name",
        )

    def get_user_input(self, args):
        if args.name == ExtensionNameEnum.BABEL:
            args.lang = self._get_input(
                default_value=args.lang,
                message="Please select the default language (default: en): ",
            )
        elif args.name == ExtensionNameEnum.CACHING:
            args.backend = self._get_input(
                default_value=args.backend,
                message=f"Please select the backend (default: {ArgumentDefaultValueEnum.REDIS_BACKEND}): ",
                choices=CachingBackendEnum.get_values(),
            )
        elif args.name == ExtensionNameEnum.LOGGING:
            args.logging_type = self._get_input(
                default_value=args.logging_type,
                message=f"Please select the log type (default: {ArgumentDefaultValueEnum.LOGGING_TYPE}): ",
                choices=LoggingTypeEnum.get_values(),
            )
        elif args.name == ExtensionNameEnum.STREAM:
            args.broker = self._get_input(
                default_value=args.broker,
                message=f"Please select the broker (default: {ArgumentDefaultValueEnum.STREAM_BROKER}): ",
                choices=StreamBrokerEnum.get_values(),
            )
        elif args.name == ExtensionNameEnum.AUTH:
            args.auth = self._get_input(
                default_value=args.auth,
                message=f"Please select the auth ext (default: {ArgumentDefaultValueEnum.AUTH}): ",
                choices=AuthEnum.get_values(),
            )
