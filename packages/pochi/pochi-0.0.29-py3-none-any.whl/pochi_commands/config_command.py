import os
from logs.manager import LoggingManager
from pochi_commands.command_interface import CommandInterface
import pochi_commands.constants as constants
import toml
from utils.helpers import Helpers


class ConfigCommand(CommandInterface):
    def __init__(self, parser):
        config_parser = parser.add_parser(
            "config",
            usage="pochi config [--name=<parameter_name> --value=<parameter_value>]",
            help=f"Update config values; if a config parameter does not already exist, add it to the project.toml file. If --name and --value are not specified, display all config parameter values.",
        )
        config_parser.add_argument(
            "--name", nargs="?", help="Specify the config parameter name"
        )
        config_parser.add_argument(
            "--value", nargs="?", help="Specify the config parameter value"
        )

    def get_help_text(self):
        help_text = """pochi config [--name=<parameter_name> --value=<parameter_value>]
    Add or update a config value in project.toml. If --name and --value are not specified, display all config parameter values.
        
    Options:
        --name=<parameter_name>                     Specify the parameter name in the project.toml. Supports hierarchy.
        --value=<parameter_value>                   Specify the parameter value.
"""
        return help_text

    def __create_dict(self, name, value):
        # print(name)
        if len(name) == 1:
            return {name.pop(): value}
        
        return { name.pop(0): self.__create_dict(name, value)}

    def execute(self, options):
        has_errors = False
        LoggingManager.display_message("pochi_header", "CONFIG")
        if os.path.isdir("config") and os.path.isfile(
            os.path.join("config", "project.toml")
        ):
            project_config_data = toml.load(os.path.join("config", "project.toml"))

            # if (hasattr(options.config, "name") and hasattr(options.config, "value")):
            if options.config.name is not None and options.config.value is not None:
                # got both values; make the update or insert into project.toml.
                config_parameter_name_list = options.config.name.split(".")
                if len(config_parameter_name_list) ==1:
                    project_config_data[options.config.name] = options.config.value
                else:
                    itemname=config_parameter_name_list.pop(0)
                    if (itemname in project_config_data):
                        # merge the existing values with the new values
                        project_config_data[itemname] = {
                            **(project_config_data[itemname]),
                            **(self.__create_dict(config_parameter_name_list, options.config.value))
                        }
                    else:
                        project_config_data[itemname] = self.__create_dict(config_parameter_name_list, options.config.value)

                # print(project_config_data)

                # project_config_data[options.config.name] = options.config.value
                with open(os.path.join("config", "project.toml"), "w") as output:
                    toml.dump(project_config_data, output)
                LoggingManager.display_message(
                    "set_config_parameter", [options.config.name, options.config.value]
                )
            elif options.config.name is None and options.config.value is None:
                # display existing config values
                # dict_project_config = vars(options.project_config)
                parameters = Helpers.toml_dict_to_string(project_config_data)
                LoggingManager.display_message(
                    "display_application_parameters", parameters
                )
            else:
                # got one or the other argument. This is not right.
                LoggingManager.display_message("parameter_config_issue")
                has_errors = True

        else:
            LoggingManager.display_message("parameter_config_issue")
            has_errors = True

        LoggingManager.display_message("closing_section")
        LoggingManager.display_message(
            "pochi_sucess", ["CONFIG", "FAILED" if has_errors else "SUCCESS"]
        )
