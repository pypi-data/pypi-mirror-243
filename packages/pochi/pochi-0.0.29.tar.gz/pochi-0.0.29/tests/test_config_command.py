import io
from unittest.mock import patch
from tests.base_test_command import BaseTestCommand


class TestConfigCommand(BaseTestCommand):
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.exit", side_effect=SystemExit)
    def test_init_output(self, mock_exit, mock_stdout):
        with self.assertRaises(SystemExit):
            self.pcm.execute_commands(["init"])

        self.clear_captured_output(mock_stdout)

        with self.assertRaises(SystemExit):
            self.pcm.execute_commands(
                ["config", "--name=default_connection", "--value=connections.DEV01"]
            )

        mock_exit.assert_called_with(0)

        output = mock_stdout.getvalue()

        with open(f"{self.expected_outputs}/test_3_output.txt") as expected_file:
            expected_file_content = expected_file.read()

        self.assertEqual(
            output,
            expected_file_content,
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.exit", side_effect=SystemExit)
    def test_update_default_connection(self, mock_exit, mock_stdout):
        with self.assertRaises(SystemExit):
            self.pcm.execute_commands(["init"])

        self.clear_captured_output(mock_stdout)

        with self.assertRaises(SystemExit):
            self.pcm.execute_commands(
                ["config", "--name=default_connection", "--value=connections.DEV01"]
            )

        with open(f"{self.generated_path}/config/project.toml") as expected_file:
            project_toml_content = expected_file.read()

        self.assertEqual(
            project_toml_content,
            """application_package_name = "generated"
application_version_name = "MyFirstVersion"
default_connection = "connections.DEV01"
application_package_distribution = "INTERNAL"
""",
        )
