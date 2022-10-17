from cgi import print_form
from genericpath import isdir
import os
from glob import glob
import click

guarded_words = ['key =', 'access_key =', 'auth_key =',
                 'password =', 'secret =', 'token =', 'access_token =']

exempted_files = ['key_guards.py']
exempted_extensions = ['.jpg', '.png']


cwd = os.getcwd()


@click.command()
@click.option('-a', '--add', help='Add a new word to the list of guarded words')
@click.option('-r', '--remove', help='Remove a word from the list of guarded words')
@click.option('-x', '--exclude', help='Exclude a file from the scan')
@click.option('-i', '--include', help='Include a file in the scan')
@click.option('-l', '--list', is_flag=True, help='List all the guarded words')
@click.option('-s', '--scan', is_flag=True, help='Scan the project for any key or token')
@click.argument('path', type=click.Path(dir_okay=True), default=cwd, required=False)
@click.argument('file', type=str, required=False)
def cli(path: str, add: bool, remove: bool, exclude: bool, include: bool, list: bool, scan: bool, file: str) -> None:
    """CLI tool to scan a project for any key or token
    """
    if scan:
        def searchText(path):

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
                    # move back to parent directory
                    os.chdir('..')
        searchText(path)
        click.echo(click.style("\nScanning completed successfully", fg='green'))

    if add:
        guarded_words.append(add)
        click.echo(click.style(
            f"Added '{add}' to the list of guarded words", fg='green'))

    if remove:
        try:
            guarded_words.remove(remove)
            click.echo(f"Removed {remove} from the list of guarded words")
        except ValueError:
            click.echo(f"{remove} not found in the list of guarded words")

    if exclude:
        exempted_files.append(exclude)
        click.echo(f"Excluded {exclude} from the scan")

    if include:
        try:
            exempted_files.remove(include)
            click.echo(f"Included {include} in the scan")
        except ValueError:
            click.echo(f"{include} not found in the list of excluded files")
    if list:
        click.echo(guarded_words)
    else:
        click.echo("Invalid command. Kindly check the help for more details")


if __name__ == '__main__':
    cli()
