import io
import os
from unittest import mock
from unittest.mock import patch
from pochi_commands.pochi_util import PochiUtil
from tests.base_test_command import BaseTestCommand


class TestCleanCommand(BaseTestCommand):
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.exit", side_effect=SystemExit)
    @patch.object(PochiUtil, "initialize_snowflake_connection", return_value=False)
    @patch.object(PochiUtil, "execute_sql_from_file", return_value=False)
    @mock.patch("builtins.open", BaseTestCommand().open)
    def test_clean_output(
        self,
        mock_execute_sql_from_file,
        mock_initialize_snowflake_connection,
        mock_exit,
        mock_stdout,
    ):
        self.template_manager.context = {
            "output_directory_path": os.path.join(
                self.generated_path, "pochi_default", "generated"
            )
        }
        with patch.object(
            PochiUtil, "execute_sql", side_effect=BaseTestCommand().execute_sql
        ):
            with self.assertRaises(SystemExit):
                self.pcm.execute_commands(
                    [
                        "init",
                        "--name=pochi_default",
                        "--version=MyFirstVersion",
                        "--connection=DEV01",
                    ]
                )

            self.pcm.execute_commands(["deploy"])

            self.pcm.execute_commands(["test"])

            self.clear_captured_output(mock_stdout)

        files_list = self.list_files(self.generated_path)

        expected_files_list = [
            f"{self.generated_path}/pochi_default/README.md",
            f"{self.generated_path}/pochi_default/generated/app/README.md",
            f"{self.generated_path}/pochi_default/generated/app/manifest.yml",
            f"{self.generated_path}/pochi_default/generated/app/sql/setup.sql",
            f"{self.generated_path}/pochi_default/generated/test/testsuite1.sql",
            f"{self.generated_path}/pochi_default/generated/deployment/deploy_application_package.sql",
            f"{self.generated_path}/pochi_default/generated/deployment/deploy_application_logic.sql",
            f"{self.generated_path}/pochi_default/generated/deployment/deploy_postinstall_objects.sql",
            f"{self.generated_path}/pochi_default/generated/deployment/deploy_preinstall_objects.sql",
            f"{self.generated_path}/pochi_default/test/testsuite1/setup.sql",
            f"{self.generated_path}/pochi_default/test/testsuite1/test01.sql",
            f"{self.generated_path}/pochi_default/test/testsuite1/teardown.sql",
            f"{self.generated_path}/pochi_default/config/project.toml",
            f"{self.generated_path}/pochi_default/src/application_package/sql/app_pkg_definition_01.sql",
            f"{self.generated_path}/pochi_default/src/application_package/sql/postinstall/postinstall_definition_01.sql",
            f"{self.generated_path}/pochi_default/src/application_package/sql/preinstall/preinstall_definition_01.sql",
            f"{self.generated_path}/pochi_default/src/application_logic/resources/README.md",
            f"{self.generated_path}/pochi_default/src/application_logic/resources/manifest.yml",
            f"{self.generated_path}/pochi_default/src/application_logic/sql/app_setup_definition_01.sql",
        ]

        self.assertEqual(expected_files_list, files_list)
        with patch.object(PochiUtil, "execute_sql", return_value=False):
            self.pcm.execute_commands(["clean"])

        output = mock_stdout.getvalue()

        expected_output = self.template_manager.render_template_from_file(
            os.path.join(self.expected_outputs, "test_8_output.txt")
        )

        self.assertEqual(expected_output, output)

        files_list = self.list_files(self.generated_path)

        expected_files_list = [
            f"{self.generated_path}/pochi_default/README.md",
            f"{self.generated_path}/pochi_default/test/testsuite1/setup.sql",
            f"{self.generated_path}/pochi_default/test/testsuite1/test01.sql",
            f"{self.generated_path}/pochi_default/test/testsuite1/teardown.sql",
            f"{self.generated_path}/pochi_default/config/project.toml",
            f"{self.generated_path}/pochi_default/src/application_package/sql/app_pkg_definition_01.sql",
            f"{self.generated_path}/pochi_default/src/application_package/sql/postinstall/postinstall_definition_01.sql",
            f"{self.generated_path}/pochi_default/src/application_package/sql/preinstall/preinstall_definition_01.sql",
            f"{self.generated_path}/pochi_default/src/application_logic/resources/README.md",
            f"{self.generated_path}/pochi_default/src/application_logic/resources/manifest.yml",
            f"{self.generated_path}/pochi_default/src/application_logic/sql/app_setup_definition_01.sql",
        ]

        self.assertEqual(expected_files_list, files_list)
