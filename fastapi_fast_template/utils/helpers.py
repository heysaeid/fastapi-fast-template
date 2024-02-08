import ast
import os
from configparser import ConfigParser

from fastapi_fast_template.utils.enums import ExtensionNameEnum


def create_directory(directory: str) -> bool:
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    return False


def create_file(
    file: str,
    file_content: str = "",
    exist_ok: bool = True,
) -> None:
    if not exist_ok or not os.path.exists(file):
        with open(file, "w") as f:
            f.write(file_content)
        return True
    return False


def find_line_in_file(value, file_path):
    with open(file_path) as file:
        for line_number, line in enumerate(file, start=1):
            if value in line:
                return line_number, line.strip()
    return None


def add_new_line(
    file_path: str,
    new_line: str,
    search_value: str = None,
    remove_matched: bool = False,
):
    with open(file_path) as file:
        if remove_matched and search_value in file.read():
            return
        lines = file.readlines()

    if not remove_matched and search_value:
        with open(file_path, "w") as file:
            for line in lines:
                if search_value in line:
                    file.write(new_line + "\n")
                file.write(line)
    else:
        with open(file_path, "a+") as file:
            file.write(new_line + "\n")


def add_line_to_last_import(file_path, new_line):
    with open(file_path) as file:
        lines = file.readlines()

    last_import_index = -1
    for i, line in enumerate(lines):
        if line.startswith("from") and "import" in line:
            last_import_index = i

    if last_import_index != -1:
        lines.insert(last_import_index + 1, new_line + "\n")

    with open(file_path, "w") as file:
        file.writelines(lines)


def get_app_config() -> dict | None:
    config = ConfigParser()
    project_root = os.getcwd()
    config.read(f"{project_root}/.fast_template.ini")
    if "app" in config:
        return config["app"]
    return


class FileBuilder:
    def __init__(
        self, file: str, build_function: callable = None, inputs: dict = None
    ):
        if inputs is None:
            inputs = {}
        self.file = file
        self.build_function = build_function
        self.inputs = inputs

    def build(self) -> bool:
        return create_file(
            file=self.file,
            file_content=self.build_function(**self.inputs)
            if self.build_function
            else "",
        )


def add_text_to_obj_end(
    file_path: str,
    text_to_add: str,
    class_name: str = None,
    function_name: str = None,
    async_function_name: str = None,
) -> None:
    try:
        # Read the module file
        with open(file_path) as file:
            code = file.read()

        # Parse the code
        tree = ast.parse(code)

        # Find the class definition
        found = False
        empty_expr = ast.Expr(ast.Name(id="", ctx=ast.Load()))
        for node in tree.body:
            # Add the desired text to the end of the class definition
            if (
                class_name
                and isinstance(node, ast.ClassDef)
                and node.name == class_name
            ):
                found = True
                node.body.append(ast.parse(text_to_add).body[0])
                node.body.append(empty_expr)
                break
            elif (
                function_name
                and isinstance(node, ast.FunctionDef)
                and node.name == function_name
            ):
                found = True
                node.body.append(ast.parse(text_to_add).body[0])
                node.body.append(empty_expr)
                break
            elif (
                async_function_name
                and isinstance(node, ast.AsyncFunctionDef)
                and node.name == async_function_name
            ):
                found = True
                node.body.append(ast.parse(text_to_add).body[0])
                node.body.append(empty_expr)
                break

        if found:
            # Rewrite the modified code back to the module file
            with open(file_path, "w") as file:
                file.write(ast.unparse(tree))
            print(
                f"Text added to the end of class '{class_name}' in module '{file_path}'"
            )
        else:
            print(f"Class '{class_name}' not found in module '{file_path}'")
    except FileNotFoundError:
        print(f"Module '{file_path}' not found")


def check_extension_exists(extension: ExtensionNameEnum | str) -> bool:
    config = get_app_config()
    if config.get(extension) is not None:
        return True
    return False
