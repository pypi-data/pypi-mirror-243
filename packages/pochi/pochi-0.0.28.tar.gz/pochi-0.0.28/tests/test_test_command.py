import io
import os
from unittest import mock
from unittest.mock import patch
from pochi_commands.pochi_util import PochiUtil
from tests.base_test_command import BaseTestCommand


class TestTestCommand(BaseTestCommand):
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.exit", side_effect=SystemExit)
    @patch.object(PochiUtil, "initialize_snowflake_connection", return_value=False)
    @patch.object(PochiUtil, "execute_sql_from_file", return_value=False)
    @patch.object(PochiUtil, "execute_sql", side_effect=BaseTestCommand().execute_sql)
    @mock.patch("builtins.open", BaseTestCommand().open)
    def test_deploy_output(
        self,
        mock_execute_sql,
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

        with self.assertRaises(SystemExit):
            self.pcm.execute_commands(
                [
                    "init",
                    "--name=pochi_default",
                    "--version=MyFirstVersion",
                    "--connection=connections.DEV01",
                ]
            )

        self.clear_captured_output(mock_stdout)

        self.pcm.execute_commands(["test"])

        mock_execute_sql_from_file.assert_called_with(
            "generated/test/testsuite1.sql", query_logging=True
        )

        with open(
            os.path.join(
                self.generated_path,
                "pochi_default",
                "generated",
                "test",
                "testsuite1.sql",
            ),
            "r",
        ) as testsuite1_file:
            testsuite1_file_content = testsuite1_file.read()
        with open(
            os.path.join(self.expected_outputs, "testsuite1.sql"), "r"
        ) as expected_testsuite1_file:
            expected_testsuite1_file_content = expected_testsuite1_file.read()
        self.assertEqual(testsuite1_file_content, expected_testsuite1_file_content)

        output = mock_stdout.getvalue()

        expected_output = self.template_manager.render_template_from_file(
            os.path.join(self.expected_outputs, "test_6_output.txt")
        )

        self.assertEqual(output, expected_output)

        files_list = self.list_files(self.generated_path)

        expected_files_list = [
            "/Users/ecuberojimenez/repositories/pochi/tests/generated/pochi_default/README.md",
            "/Users/ecuberojimenez/repositories/pochi/tests/generated/pochi_default/generated/test/testsuite1.sql",
            "/Users/ecuberojimenez/repositories/pochi/tests/generated/pochi_default/test/testsuite1/setup.sql",
            "/Users/ecuberojimenez/repositories/pochi/tests/generated/pochi_default/test/testsuite1/test01.sql",
            "/Users/ecuberojimenez/repositories/pochi/tests/generated/pochi_default/test/testsuite1/teardown.sql",
            "/Users/ecuberojimenez/repositories/pochi/tests/generated/pochi_default/config/project.toml",
            "/Users/ecuberojimenez/repositories/pochi/tests/generated/pochi_default/src/application_package/sql/app_pkg_definition_01.sql",
            "/Users/ecuberojimenez/repositories/pochi/tests/generated/pochi_default/src/application_package/sql/postinstall/postinstall_definition_01.sql",
            "/Users/ecuberojimenez/repositories/pochi/tests/generated/pochi_default/src/application_package/sql/preinstall/preinstall_definition_01.sql",
            "/Users/ecuberojimenez/repositories/pochi/tests/generated/pochi_default/src/application_logic/resources/README.md",
            "/Users/ecuberojimenez/repositories/pochi/tests/generated/pochi_default/src/application_logic/resources/manifest.yml",
            "/Users/ecuberojimenez/repositories/pochi/tests/generated/pochi_default/src/application_logic/sql/app_setup_definition_01.sql",
        ]

        self.assertEqual(expected_files_list, files_list)
