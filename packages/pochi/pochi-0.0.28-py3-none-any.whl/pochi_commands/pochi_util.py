import snowflake.connector
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
from logs.manager import LoggingManager
import getpass
import traceback
import configparser
from pathlib import Path
from platformdirs import PlatformDirs
import argparse
import toml


class PochiUtil:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PochiUtil, cls).__new__(cls)
            cls._instance.init_data()
        return cls._instance

    def init_data(self):
        self.__connection = None
        self.__connections_list = {}

    def __load_connection_config(self, connection_name):
        # Step 2: Load the Snowflake connections files to look up the project's connection target
        # Snowflake has two types of config files that can be loaded:
        # (1) SnowCLI (https://docs.snowflake.com/LIMITEDACCESS/snowcli/connecting/connect)
        # (2) SnowSQL (https://docs.snowflake.com/en/user-guide/snowsql-config)
        #
        # Pochi searches for connection using the following list of config files:
        # (1) ~/.snowflake/config.toml (if it exists)
        # (2) Snowflake app directory/config.toml (if it exists)
        # (3) ~/.snowsql/config (regular config file, not TOML)
        #
        # There may be other locations but Pochi only supports the above 3 locations at this point.

        # Find SnowCLI config file and use it.
        snowcli_config_toml = os.path.join(os.environ.get("SNOWFLAKE_HOME", os.path.join(Path.home(), ".snowflake")), "config.toml")
        
        if not os.path.exists(snowcli_config_toml):
            snowcli_config_toml = os.path.join(
                PlatformDirs(appname="snowflake", appauthor=False).user_config_path,
                "config.toml"
            )

        snowsql_config = os.path.join(Path.home(), ".snowsql", "config")
        connection_config = None
        connection_config_namespace = None
        if snowcli_config_toml is not None and os.path.exists(snowcli_config_toml):
            # Found the SnowCLI connection toml file; load it!
            connection_config = toml.load(snowcli_config_toml)
            default_connection_config = connection_config.get("connections").get(
                connection_name, None
            )
            connection_config_namespace = argparse.Namespace()
            setattr(
                        connection_config_namespace,
                        "connection_name",
                        connection_name,
                    )
            setattr(
                        connection_config_namespace,
                        "connection_file_path",
                        snowcli_config_toml,
                    )
            if default_connection_config is not None:
                setattr(
                        connection_config_namespace,
                        "is_defined",
                        True,
                )
                for parameter in default_connection_config:
                    setattr(
                        connection_config_namespace,
                        parameter,
                        default_connection_config[parameter],
                    )
            else:
                setattr(
                        connection_config_namespace,
                        "is_defined",
                        False,
                )

        elif os.path.exists(snowsql_config):
            connection_config = configparser.ConfigParser()
            connection_config.read(snowsql_config)

            connection_section_name = "connections." + connection_name
            connection_config_namespace = argparse.Namespace()
            setattr(
                        connection_config_namespace,
                        "connection_name",
                        connection_name,
                    )
            setattr(
                        connection_config_namespace,
                        "connection_file_path",
                        snowsql_config,
                    )
            if connection_config.has_section(connection_section_name):
                setattr(
                        connection_config_namespace,
                        "is_defined",
                        True,
                )
                default_connection_config = connection_config[connection_section_name]
                if ("accountname" in default_connection_config):
                    setattr(
                        connection_config_namespace,
                        "account",
                        default_connection_config["accountname"],
                    )
                if ("username" in default_connection_config):
                    setattr(
                        connection_config_namespace,
                        "user",
                        default_connection_config["username"],
                    )
                if ("password" in default_connection_config):
                    setattr(
                        connection_config_namespace,
                        "password",
                        default_connection_config["password"],
                    )
                if ("rolename" in default_connection_config):
                    setattr(
                        connection_config_namespace,
                        "role",
                        default_connection_config["rolename"],
                    )
                if ("warehousename" in default_connection_config):
                    setattr(
                        connection_config_namespace,
                        "warehouse",
                        default_connection_config["warehousename"],
                    )
                if ("private_key_path" in default_connection_config):
                    setattr(
                        connection_config_namespace,
                        "private_key_path",
                        default_connection_config["private_key_path"],
                    )
            else:
                setattr(
                        connection_config_namespace,
                        "is_defined",
                        False,
                )
        return connection_config_namespace

    def __get_snowflake_connection(self, connection_name):
        snowflake_connection = None
        connection_config = None
        try:
            if (connection_name is None):
                return None

            connection_config = self.__load_connection_config(connection_name)

            # 3. default_connection is defined in the config/project.toml, but the name is not defined in the
            #    connection config file. return error
            if (not connection_config.is_defined):
                LoggingManager.display_message(
                    "invalid_connection_name_issue",
                    [connection_config.connection_name,
                    connection_config.connection_file_path]
                )
                return None

            # 4. if accountname is missing, or username is missing, return error.
            if ("account" not in connection_config or
                 "user" not in connection_config):
                LoggingManager.display_message(
                            "missing_parameters_connection_issue",
                        )
                return None
            
            # authentication sequence:
            # if private_key_path exists, then use private_key_path.
            # otherwise, if password exists, then use the password, else ask for password
            if ("private_key_path" in connection_config):
                # this connection is using a private_key_path
                if (os.getenv ("SNOWSQL_PRIVATE_KEY_PASSPHRASE") is None):
                    LoggingManager.display_message(
                            "missing_private_key_passphrase_connection_issue",
                        )
                    return None
                
                with open(connection_config.private_key_path, "rb") as key:
                    p_key = serialization.load_pem_private_key(
                        key.read(),
                        password=os.getenv("SNOWSQL_PRIVATE_KEY_PASSPHRASE").encode(),
                        backend=default_backend(),
                    )

                pkb = p_key.private_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )

                snowflake_connection = snowflake.connector.connect(
                    user=connection_config.user,
                    account=connection_config.account,
                    private_key=pkb,
                    role=getattr(connection_config, "role", None),
                    warehouse=getattr(connection_config, "warehouse", None)
                )
            else:
                # this connection has user and password defined in the config. Use them directly.
                connection_password = None
                if ("password" in connection_config):
                    connection_password = connection_config.password
                else:
                    connection_password = getpass.getpass(prompt="Enter Password for Connection " + connection_config.connection_name + ": ")

                snowflake_connection = snowflake.connector.connect(
                    user=connection_config.user,
                    password=connection_password,
                    account=connection_config.account,
                    role=getattr(connection_config, "role", None),
                    warehouse=getattr(connection_config, "warehouse", None)
                )

        except snowflake.connector.Error as e:
            LoggingManager.display_message(
                "connection_issues",
                [
                    connection_config.account,
                    connection_config.connection_name,
                ],
            )
            LoggingManager.display_single_message(
                e
            )
        except Exception as e:
            LoggingManager.display_single_message(
                f"Unexpected {type(e)=}: {e=}"
            )
            LoggingManager.display_single_message(traceback.format_exc())
        finally:
            if snowflake_connection is not None:
                LoggingManager.display_single_message(
                    "Initializing Connection {0} to Account {1} using config file {2}".format(
                    connection_config.connection_name,
                    connection_config.account,
                    connection_config.connection_file_path
                    )
                )
            return snowflake_connection


    def initialize_snowflake_connection(self, connection_name):
        # 1. self.__connection already exists; return (no errors)
        if (connection_name in self.__connections_list):
            self.__connection = self.__connections_list[connection_name]
            return False

        new_connection = self.__get_snowflake_connection(connection_name)
        if (new_connection is None):
            return True
        self.__connections_list[connection_name] = new_connection
        self.__connection = new_connection
        return False



    def execute_sql(self, sql_statement, with_output=False):
        has_errors = False
        try:
            cur = self.__connection.cursor().execute(sql_statement)
            if self.__connection.get_query_status(cur.sfqid).name != "SUCCESS":
                has_errors = True
        except Exception as e:
            LoggingManager.display_message(
                "script_issues",
                [
                    sql_statement,
                    e,
                ],
            )
            LoggingManager.display_single_message(traceback.format_exc())
            has_errors = True
        finally:
            if with_output:
                return has_errors, cur.fetchall()
            return has_errors

    def execute_sql_from_file(self, file_path, has_errors=False, query_logging=False, testsuite=None):
        try:
            if os.path.exists(file_path) and not has_errors:
                with open(file_path, "r") as sql_file:
                    for cur in self.__connection.execute_stream(
                        sql_file, remove_comments=True
                    ):
                        if query_logging:
                            col_width = 39 if len(cur.description) > 1 else 121
                            LoggingManager.display_single_message(
                                "[SQL] +-"
                                + "+-".join("-" * col_width for col in cur.description)
                                + "+"
                            )
                            LoggingManager.display_single_message(
                                # "[SQL] | " + "| ".join(str(col.name)[:col_width].ljust(col_width) for col in cur.description) + "|"
                                "[SQL] | "
                                + "| ".join(
                                    str(col.name)[:col_width].ljust(col_width)
                                    for col in cur.description
                                )
                                + "|"
                            )
                            LoggingManager.display_single_message(
                                "[SQL] +-"
                                + "+-".join("-" * col_width for col in cur.description)
                                + "+"
                            )
                            for ret in cur:
                                LoggingManager.display_single_message(
                                    # "[SQL] | " + "| ".join(str(col)[:col_width].ljust(col_width) for col in ret) + "|"
                                    "[SQL] | "
                                    + "| ".join(
                                        str(col).ljust(col_width) for col in ret
                                    )
                                    + "|"
                                )
                            LoggingManager.display_single_message(
                                "[SQL] +-"
                                + "+-".join("-" * col_width for col in cur.description)
                                + "+"
                            )
                            LoggingManager.display_single_message("[SQL] ")
                        if (
                            self.__connection.get_query_status(cur.sfqid).name
                            != "SUCCESS"
                        ):
                            has_errors = True
        except snowflake.connector.Error as e:
            LoggingManager.display_message(
                "script_issues",
                [
                    file_path,
                    e,
                ],
            )
            has_errors = True
        except Exception as e:
            LoggingManager.display_message(
                "script_issues",
                [
                    file_path,
                    e,
                ],
            )
            LoggingManager.display_single_message(traceback.format_exc())
            has_errors = True
        finally:
            return has_errors
