import os
from glob import glob
import click


cwd = os.getcwd()


@click.command(name='Key Guard')
@click.option('-i', '--init', is_flag=True, help='Initialize the key_guard')
@click.option('-s', '--scan', is_flag=True, help='Scan the project for any key or token')
@click.option('-l', '--list', is_flag=True, help='List all the guarded words')
@click.option('-e', '--exempt', nargs=1, help='exempt a file from scanning by removing from .guard/.fileignore')
@click.option('-inc', '--include', nargs=1, help='include a word to scan by adding it to .guard/.fileignore')
@click.option('--add', '-a', nargs=1, help='Add new words to .guard/.keyignore')
@click.argument('path', type=click.Path(dir_okay=True), default=cwd, required=False)
# @click.argument('add', type=str, required=False)
def cli(path: str,  list: str, scan: bool, add: str, init: bool, exempt: str, include: str) -> None:
    """CLI tool to scan a project for any key or token
    """
    if init:
        # create .guard folder and create .fileignore and .keyignore files
        try:
            os.mkdir('.guard')
            os.chdir('.guard')
            click.secho("Initializing the key_guard", fg='green')
            click.secho("Creating .guardignore files", fg='green')
            with open('.fileignore', 'w') as f:
                f.writelines(['.git\n', '.guard\n', '.vscode\n', '.idea\n', '.pytest_cache\n',
                              '__pycache__\n', 'venv\n', 'node_modules\n', '.env\n', '.venv\n'])
                f.close()

            with open('.keyignore', 'w') as f:
                f.writelines(['key =\n', 'access_key =\n', 'auth_key =\n',
                              'password =\n', 'secret =\n', 'token =\n', 'access_token =\n'])
                f.close()
        except FileExistsError:
            click.secho("key_guard is already initialized", fg='yellow')
            pass

    if scan:
        def searchText(path):
            guarded_words = [str(word.strip())
                             for word in open('.guard/.keyignore').readlines()]
            exempted_files = [str(file.strip())
                              for file in open('.guard/.fileignore').readlines()]

            os.chdir('..')
            os.chdir(path)
            path = os.listdir(path)
            for fname in path[::-1]:
                abs_path = os.path.abspath(fname)
                if os.path.isfile(abs_path):
                    try:
                        if os.path.basename(fname) not in exempted_files and not os.path.basename(fname).startswith('.'):
                            for l_no, line in enumerate(open(fname, 'r')):
                                for word in guarded_words:
                                    if word in line:
                                        click.echo(click.style(
                                            f"Warning: '{word}' found in `{fname.split('/')[-1]}` Kindly check for line: `{l_no}` -> '{line.strip()}' to make sure you don't commit sensitive data.", fg='yellow'))
                            path.remove(os.path.basename(fname))
                    except UnicodeDecodeError:
                        pass
                elif os.path.isdir(abs_path) and not os.path.basename(abs_path).startswith('.'):
                    print(f"Scanning {abs_path}")
                    searchText(abs_path)
                    path.remove(os.path.basename(abs_path))
                    os.chdir('..')
        searchText(path)
        click.echo(click.style("\nScanning completed successfully", fg='green'))

    if list:
        guarded_words = [str(word.strip())
                         for word in open('.guard/.keyignore').readlines()]
        click.echo(guarded_words)

    # add new words to .guard/.keyignore
    if add:
        guarded_words = [str(word.strip())
                         for word in open('.guard/.keyignore').readlines()]
        try:
            with open('.guard/.keyignore', 'a') as f:
                if add not in guarded_words:
                    f.write(f"{add}\n")
                    f.close()
                    click.secho(
                        f"Added `{add}` to .keyignore", fg='green')
                else:
                    click.secho(
                        f"`{add}` already exists in .guard/.keyignore", fg='yellow')
        except FileNotFoundError:
            click.secho("Please initialize the key_guard first", fg='red')

    if exempt:
        exempted_files = [str(file.strip())
                          for file in open('.guard/.fileignore').readlines()]
        try:
            with open('.guard/.fileignore', 'a') as f:
                if exempt not in exempted_files:
                    f.write(f"{exempt}\n")
                    f.close()
                    click.secho(
                        f"Added `{exempt}` to .fileignore", fg='green')
                else:
                    click.secho(
                        f"`{exempt}` already exists in .guard/.fileignore", fg='yellow')
        except FileNotFoundError:
            click.secho("Please initialize the key_guard first", fg='red')

    if include:
        exempted_files = [str(file.strip())
                          for file in open('.guard/.fileignore').readlines()]
        try:
            with open('.guard/.fileignore', 'r') as f:
                lines = f.readlines()
                f.close()
            with open('.guard/.fileignore', 'w') as f:
                for line in lines:
                    if line.strip("\n") != include:
                        f.write(line)
                    else:
                        lines.remove(line)
                        exempted_files.remove(line.strip("\n"))
                        click.secho(
                            f"Removed `{include}` from .fileignore", fg='green')

                f.close()
        except FileNotFoundError:
            click.secho("Please initialize the key_guard first", fg='red')
    elif not init and not scan and not list and not add and not exempt and not include:
        click.secho(
            "Welcome to key_guard! Use the `--help` option for the list of options and commands available for this tool.", fg='green')


if __name__ == '__main__':
    cli()
