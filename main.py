"""
Main module for the Simple TODO Checker.
"""

import os
import sys
import re
import argparse

# Global Environmnet Variables
os.environ["WORKSPACE"] = os.getcwd()

# Regular expressions to match TODOs in comments across various languages
global TODO_PATTERNS
TODO_PATTERNS = [
    r"#\s*todo\s*:",  # Python, JavaScript, HTML, C/C++, Java, Shell
    r"//\s*todo\s*:",  # C/C++
    r"/\*\s*todo\s*\*/",  # C/C++
    r"--\s*todo\s*;",  # Shell
    r"\{\|\s*todo\s*\|\}",  # Twig
    r"%\{\s*todo\s*\}",  # Twig
    r"<\!--\s*todo\s*-->",  # HTML
    r"\{\{\-\s*todo\s*\-\}\}",  # Twig
]

# Default list of supported file extensions
DEFAULT_EXTENSIONS = [
    ".py",
    ".js",
    ".html",
    ".css",
    ".php",
    ".cs",
    ".cpp",
    ".java",
    ".sh",
    ".twig",
    ".yml",
    ".yaml",
]


class TodoChecker:
    """
    This is the main class for the Simple TODO Checker.
    It takes a path and a list of file extensions to check for TODOs.
    It recursively searches the given path for files with the specified extensions
    """

    def __init__(self, path=".", extensions=DEFAULT_EXTENSIONS):
        self.path = path
        self.extensions = extensions

    def find_todos(self):
        """
        This method finds all TODOs in the specified path and returns a list of them.
        It uses regular expressions to match TODOs in comments across various languages.
        It attempts to open the files with UTF-8 encoding first, but if that fails,
        it falls back to 'ISO-8859-1' encoding.

        :return: A list of strings representing the TODOs found in the files.
        :rtype: list
        """

        todos = []
        todo_regex = re.compile("|".join(TODO_PATTERNS), re.IGNORECASE)

        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(self.extensions):
                    file_path = os.path.join(root, file)

                    # Attempt to open the file with UTF-8 encoding first
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            for i, line in enumerate(f, 1):
                                if todo_regex.search(line):
                                    todos.append(
                                        f"{file_path} (Line {i}): {line.strip()}"
                                    )

                    # Fallback to 'ISO-8859-1' if UTF-8 decoding fails
                    except UnicodeDecodeError:
                        with open(file_path, "r", encoding="ISO-8859-1") as f:
                            for i, line in enumerate(f, 1):
                                if todo_regex.search(line):
                                    todos.append(
                                        f"{file_path} (Line {i}): {line.strip()}"
                                    )

        return todos


if __name__ == "__main__":
    """
    This is the main entry point for the Simple TODO Checker.
    It parses command-line arguments and calls the TodoChecker class to find TODOs.
    If TODOs are found, it prints them and exits with an error code.
    """
    parser = argparse.ArgumentParser(description="Simple TODO Checker")
    parser.add_argument(
        "--path", type=str, default=".", help="Enter the path for checking for TODOs."
    )
    parser.add_argument(
        "--extensions",
        type=str,
        default=DEFAULT_EXTENSIONS,
        help="Comma-separated list of file extensions to check (e.g., .py,.js,.html)",
    )
    parser.add_argument(
        "--todo_pattern",
        type=str,
        default=TODO_PATTERNS,
        help="Custom regular expression to detect your TODOs.",
    )
    parser.add_argument(
        "--is_local",
        type=bool,
        default=False,
        help="Configure local run",
    )
    args = parser.parse_args()

    # Split extensions input into a tuple for file filtering
    try:
        extensions = tuple(args.extensions.split(","))
    except AttributeError:
        extensions = tuple(DEFAULT_EXTENSIONS)

    # Getting GH Actions Environment Variables
    if os.environ.get("INPUT_PATH") is not None:
        path = os.environ.get("INPUT_PATH")
    if os.environ.get("INPUT_EXTENSIONS") is not None:
        extensions = tuple(os.environ.get("INPUT_EXTENSIONS").split(", "))
    if os.environ.get("INPUT_TODO_PATTERN") is not None:
        TODO_PATTERNS = [os.environ.get("INPUT_TODO_PATTERN")]

    list_of_todos = TodoChecker(path=path, extensions=extensions).find_todos()

    if list_of_todos:
        print("Found TODO's in the following files: ")
        for todo in list_of_todos:
            print(todo)
        sys.exit(1)  # Exit with error to fail the action if TODOs are found
    else:
        print("No TODOs found!")
