# Simple TODO Checker

[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-Simple%20Todo%20Checker-blue?logo=github)](https://github.com/marketplace/actions/simple-todo-checker)
![Code Quality Linter](https://github.com/damienjburks/simple-todo-checker/actions/workflows/linter.yml/badge.svg)
![Docker Publish](https://github.com/damienjburks/simple-todo-checker/actions/workflows/publish-image.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/damienjburks/simple-todo-checker/badge.svg?branch=main)](https://coveralls.io/github/damienjburks/simple-todo-checker?branch=main)
![Unit Tests](https://github.com/damienjburks/simple-todo-checker/actions/workflows/unittests.yml/badge.svg)

**Simple TODO Checker** is a GitHub Action that scans code for `TODO` comments across various languages and file types, helping developers manage their in-code TODOs in a multi-language repository. This action can handle different comment syntaxes for `TODO` across many popular programming languages and file formats.

## Features

- **Multi-language Support**: Detects TODO comments in Python, JavaScript, HTML, CSS, PHP, C#, C++, Java, Shell, and Twig.
- **Flexible Encoding**: Automatically handles files with different encodings (UTF-8 and ISO-8859-1).
- **Configurable**: Allows users to specify paths and file types to scan for TODOs.
- **Detailed Output**: Provides the file path and line number for each detected TODO comment.

## How It Works

The core of Simple TODO Checker is the `TodoChecker` class, which recursively scans files in a given directory, matches TODO comments using regular expressions, and outputs the results.

### Key Code Components

- **TODO Patterns**: A set of regular expressions (`TODO_PATTERNS`) designed to capture TODO comments across various comment styles and languages.
- **Default Extensions**: A default list of file extensions (`DEFAULT_EXTENSIONS`) supported by the checker.
- **Encoding Fallbacks**: Tries to read files in UTF-8 encoding, but falls back to ISO-8859-1 if an encoding error occurs.

### Supported TODO Patterns

This action supports the following comment styles for detecting TODO comments:

```python
TODO_PATTERNS = [
    r"#\s*todo\s*:",       # Python, JavaScript, HTML, C/C++, Java, Shell
    r"//\s*todo\s*:",      # C/C++
    r"/\*\s*todo\s*\*/",   # C/C++
    r"--\s*todo\s*;",      # Shell
    r"\{\|\s*todo\s*\|\}", # Twig
    r"%\{\s*todo\s*\}",    # Twig
    r"<\!--\s*todo\s*-->", # HTML
    r"\{\{\-\s*todo\s*\-\}\}", # Twig
]
```

### Example Output

Upon detecting TODO comments, Simple TODO Checker outputs the results in the format:

```text
Found TODO's in the following files:
src/app.py (Line 23): # TODO: Implement feature X
src/index.js (Line 45): // TODO: Refactor this function
```

If no TODO comments are found, it will output:

```text
No TODOs found!
```

## Usage

To use this action in your workflow, please add the following step below:

```yaml
name: TODO Checker

on:
  pull_request:

jobs:
  find-todos:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Simple TODO Checker
        uses: damienjburks/simple-todo-checker@x.x.x
        with:
          path: "." # Scan default folder as this is required.
```

I highly recommend that you only run this action during pull requests, since it'll fail when it finds TODO comments.

### Configuration

You can configure the action further by providing the following inputs:

| Input              | Description                                                                     | Required |
| ------------------ | ------------------------------------------------------------------------------- | -------- |
| **`path`**         | File directory path for checking TODOs.                                         | Yes      |
| **`extensions`**   | Comma-separated list of file extensions to check (e.g., `.py`, `.js`, `.html`). | No       |
| **`todo_pattern`** | Custom regular expression to detect your TODOs.                                 | No       |

## Contributing

If you encounter any issues, please feel free to raise an issue or submit a PR. Anyone who wishes to contribute is encouraged to do so. If interested, please review the [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License.
