# key-guard

A python tool that checks to find exposed authentication keys in a project and throws a warning. This prevents the sharing of sensitive data and enforces the use of best practices like saving authentication keys to .env files.

## Features

- [x] Scan Project for exposed keys and passwords
- [x] Add words to guarded_words list to look out for when scanning
- [x] Exclude files from scanning
- [x] Include files for scanning

## Core Requirements

- Click

## Using the CLI tool from Pip

- Install the tool from pip by running:

```bash
pip install key-guard
```

- Quickly Scan your working directory by running:

```bash
key-guard -s
```

- Start by initializing the tool by running:

```bash
key-guard -i
```

- Add the `--help` option the command to check out the available options.

```bash
Usage: key_guard.py [OPTIONS] [PATH]

  CLI tool to scan a project for any key or token

Options:
  -e, --exempt TEXT     exempt a file from scanning by removing from
                        .guard/.fileignore
  -inc, --include TEXT  include a word to scan by adding it to
                        .guard/.fileignore
  -a, --add TEXT        Add new words to .guard/.keyignore
  -i, --init            Initialize the key_guard
  -l, --list            List all the guarded words
  -s, --scan            Scan the project for any key or token
  --help                Show this message and exit.
```

## Setting up the tool for local development

- Clone this repository to your local machine.
- Create a virtual environment for your project and activate it. Install all dependencies from  requirements.txt file.

```bash
python3 -m venv .venv/
source .venv/bin/activate
pip install -r requirements.txt
```
  
- In the root directory of the project, develop the project locally from the setup configuration.
  
```bash
python3 setup.py develop
```

- A `*.egg-info` directory is created in your root directory for you to use the tool locally. Get started by running the following command:

```bash
key-guard -i
```

- the `--help` option the command to check out the available options.

```bash
Usage: key_guard.py [OPTIONS] [PATH]

  CLI tool to scan a project for any key or token
  
Options:
-e, --exempt TEXT     exempt a file from scanning by removing from
                        .guard/.fileignore
  -inc, --include TEXT  include a word to scan by adding it to
                        .guard/.fileignore
  -a, --add TEXT        Add new words to .guard/.keyignore
  -i, --init            Initialize the key_guard
  -l, --list            List all the guarded words
  -s, --scan            Scan the project for any key or token
  --help                Show this message and exit.
```

## Contributing

- Fork this repository to your GitHub account.
- Clone the forked repository to your local machine.
- Create a new branch for the feature you want to work on.
- Make your contributions.
- Push your local branch to your remote repository.
- Open a pull request to the develop branch of this repository.

