import argparse
import importlib
import os
import sys
from logs.manager import LoggingManager

from pochi_commands.build_command import BuildCommand
from pochi_commands.clean_command import CleanCommand
from pochi_commands.config_command import ConfigCommand
from pochi_commands.deploy_command import DeployCommand
from pochi_commands.init_command import InitCommand
from pochi_commands.pochi_commands import PochiCommandManager
import logging
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from pochi_commands.test_command import TestCommand


class CommandContainer(containers.DeclarativeContainer):
    def snake_to_camel(snake_str):
        parts = snake_str.split("_")
        camel_str = "".join(word.capitalize() for word in parts)
        return camel_str

    def create_dot_pochi(path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    try:
        parser = argparse.ArgumentParser(add_help=False)
        subparsers = parser.add_subparsers(title="Available Targets")
        subparsers.add_parser("help", help="Display Help")

        dict_commands = {
            "init_command": None,
            "config_command": None,
            "clean_command": None,
            "build_command": None,
            "deploy_command": None,
            "test_command": None,
        }

        user_home = os.path.expanduser("~")
        dot_pochi_path = os.path.join(user_home, ".pochi")
        create_dot_pochi(dot_pochi_path)
        class_files = [
            file for file in os.listdir(dot_pochi_path) if file.endswith(".py")
        ]
        for class_file in class_files:
            file_name = os.path.splitext(class_file)[0]
            spec = importlib.util.spec_from_file_location(
                file_name, os.path.join(dot_pochi_path, class_file)
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            class_name = snake_to_camel(file_name)
            my_class = getattr(module, class_name)
            dict_commands[file_name] = my_class(subparsers)

        if dict_commands["init_command"] is None:
            dict_commands["init_command"] = InitCommand(subparsers)
        if dict_commands["config_command"] is None:
            dict_commands["config_command"] = ConfigCommand(subparsers)
        if dict_commands["clean_command"] is None:
            dict_commands["clean_command"] = CleanCommand(subparsers)
        if dict_commands["build_command"] is None:
            dict_commands["build_command"] = BuildCommand(subparsers)
        if dict_commands["deploy_command"] is None:
            dict_commands["deploy_command"] = DeployCommand(subparsers)
        if dict_commands["test_command"] is None:
            dict_commands["test_command"] = TestCommand(subparsers)

        command_providers = providers.Dict(dict_commands)

        pochi_command_manager = providers.Factory(
            PochiCommandManager,
            command_providers=command_providers,
            subparsers=subparsers,
            parser=parser,
        )
    except Exception as e:
        LoggingManager.display_message("error_loading_command_classes")


# Configure logger to also write to stdout
root = logging.getLogger()
root.setLevel(logging.ERROR)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.ERROR)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)


@inject
def main(
    pochi_command_manager: PochiCommandManager = Provide[
        CommandContainer.pochi_command_manager
    ],
):
    argument_list = [
        word if word not in ["--help", "-h", "-help"] else "help"
        for word in sys.argv[1:]
    ]
    pochi_command_manager.execute_commands(argument_list or ["help"])


if __name__ == "pochi_commands":
    container = CommandContainer()
    container.init_resources()
    container.wire(modules=[__name__])
