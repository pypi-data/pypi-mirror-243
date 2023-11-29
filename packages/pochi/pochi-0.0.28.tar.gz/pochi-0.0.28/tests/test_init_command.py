import io
import os
import unittest
from unittest.mock import patch
from tests.base_test_command import BaseTestCommand


class TestInitCommand(BaseTestCommand):
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.exit", side_effect=SystemExit)
    def test_init_output(self, mock_exit, mock_stdout):
        self.template_manager.context = {"generated_path": self.generated_path}

        with self.assertRaises(SystemExit):
            self.pcm.execute_commands(["init"])

        mock_exit.assert_called_with(0)

        output = mock_stdout.getvalue()

        expected_output = self.template_manager.render_template_from_file(
            os.path.join(self.expected_outputs, "test_1_output.txt")
        )

        self.assertEqual(
            output,
            expected_output,
        )

    def test_init_directory_structure(self):
        with self.assertRaises(SystemExit):
            self.pcm.execute_commands(["init"])

        files_list = self.list_files(self.generated_path)
        expected_files_list = [
            f"{self.generated_path}/README.md",
            f"{self.generated_path}/test/testsuite1/setup.sql",
            f"{self.generated_path}/test/testsuite1/test01.sql",
            f"{self.generated_path}/test/testsuite1/teardown.sql",
            f"{self.generated_path}/config/project.toml",
            f"{self.generated_path}/src/application_package/sql/app_pkg_definition_01.sql",
            f"{self.generated_path}/src/application_package/sql/postinstall/postinstall_definition_01.sql",
            f"{self.generated_path}/src/application_package/sql/preinstall/preinstall_definition_01.sql",
            f"{self.generated_path}/src/application_logic/resources/README.md",
            f"{self.generated_path}/src/application_logic/resources/manifest.yml",
            f"{self.generated_path}/src/application_logic/sql/app_setup_definition_01.sql",
        ]
        self.assertEqual(expected_files_list, files_list)


if __name__ == "__main__":
    unittest.main()
