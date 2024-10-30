import os
import argparse
import tempfile
import unittest
from unittest.mock import patch

from src.todo_checker import TodoChecker, main


class TestTodoChecker(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file_path = os.path.join(self.test_dir.name, "test.py")
        with open(self.test_file_path, "w") as f:
            f.write("# TODO: Fix this issue\n")
            f.write("# This is a test file with a TODO comment\n")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_find_todos_with_default_patterns(self):
        checker = TodoChecker(
            path=self.test_dir.name,
            extensions=(".py",),
            todo_patterns=[r"#\s*todo\s*:"],
        )
        todos = checker.find_todos()
        self.assertIn(f"{self.test_file_path} (Line 1): # TODO: Fix this issue", todos)

    def test_find_todos_with_multiple_patterns(self):
        checker = TodoChecker(
            path=self.test_dir.name,
            extensions=(".py",),
            todo_patterns=[r"#\s*todo\s*:", r"//\s*todo\s*:"],
        )
        todos = checker.find_todos()
        self.assertEqual(len(todos), 1)
        self.assertIn(f"{self.test_file_path} (Line 1): # TODO: Fix this issue", todos)

    def test_no_todos_found(self):
        with open(self.test_file_path, "w") as f:
            f.write("# This file has no TODOs\n")
        checker = TodoChecker(
            path=self.test_dir.name,
            extensions=(".py",),
            todo_patterns=[r"#\s*todo\s*:"],
        )
        todos = checker.find_todos()
        self.assertEqual(len(todos), 0)


class TestMain(unittest.TestCase):
    @patch("sys.exit")
    @patch("builtins.print")
    @patch("argparse.ArgumentParser.parse_args")
    def test_todos_found_exit_code(self, mock_parse_args, mock_print, mock_exit):
        # Mock command-line arguments and environment variables
        mock_parse_args.return_value = argparse.Namespace(
            path="test_dir",
            extensions=".py,.js",
            todo_pattern=["#\\s*todo\\s*:"],
            is_local=False,
        )

        # Mock environment variables if needed
        os.environ["INPUT_PATH"] = "test_dir"
        os.environ["INPUT_EXTENSIONS"] = ".py,.js"
        os.environ["INPUT_TODO_PATTERN"] = "#\\s*todo\\s*:"

        # Mock the TodoChecker to simulate finding TODOs
        with patch.object(
            TodoChecker,
            "find_todos",
            return_value=["file1.py (Line 1): # TODO: Example"],
        ):
            main()

            # Assert sys.exit(1) was called since TODOs were found
            mock_exit.assert_called_once_with(1)
            mock_print.assert_any_call("Found TODO's in the following files: ")
            mock_print.assert_any_call("file1.py (Line 1): # TODO: Example")

    @patch("sys.exit")
    @patch("builtins.print")
    @patch("argparse.ArgumentParser.parse_args")
    def test_no_todos_found_exit_code(self, mock_parse_args, mock_print, mock_exit):
        # Mock command-line arguments
        mock_parse_args.return_value = argparse.Namespace(
            path="test_dir",
            extensions=".py,.js",
            todo_pattern=["#\\s*todo\\s*:"],
            is_local=False,
        )

        # Mock environment variables if needed
        os.environ["INPUT_PATH"] = "test_dir"
        os.environ["INPUT_EXTENSIONS"] = ".py,.js"
        os.environ["INPUT_TODO_PATTERN"] = "#\\s*todo\\s*:"

        # Mock the TodoChecker to simulate no TODOs found
        with patch.object(TodoChecker, "find_todos", return_value=[]):
            main()

            # Assert sys.exit(0) was called since no TODOs were found
            mock_print.assert_called_once_with("No TODOs found!")


if __name__ == "__main__":
    unittest.main()
