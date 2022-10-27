import os
import click


cwd = os.getcwd()



#load exempted files and keys to guard
def load_from_files(fileignore_path,keyignore_path):
    '''
    load contents of .fileignore and .keyignore and return them in a dict object  
    '''
    try:
        guarded_words = [str(word.strip())
                            for word in open(keyignore_path).readlines()]
        exempted_files = [str(file.strip())
                        for file in open(fileignore_path).readlines()]
        return {"guarded_words":guarded_words, "exempted_files":exempted_files}
    except FileNotFoundError:
        click.echo(click.style("\nmake sure key-guard is initialized\n", fg='red'))





#seach text method used in scanning
def  searchText(path,fileignore_path,keyignore_path):
    file_contents = load_from_files(fileignore_path,keyignore_path)  #loading contents from .fileignore and .keyignore into a dict object
    os.chdir('..')
    os.chdir(path)
    path = os.listdir(path)
    for fname in path[::-1]:
        abs_path = os.path.abspath(fname)
        if os.path.isfile(abs_path):
            try:
                if os.path.basename(fname) not in file_contents["exempted_files"] and not os.path.basename(fname).startswith('.'):
                    for l_no, line in enumerate(open(fname, 'r')):
                        for word in file_contents["guarded_words"]:
                            if word in line:
                                click.echo(click.style(
                                        f"Warning: '{word}' found in `{fname.split('/')[-1]}` Kindly check for line: `{l_no}` -> '{line.strip()}' to make sure you don't commit sensitive data.", fg='yellow'))
                                        
                    path.remove(os.path.basename(fname))
            except UnicodeDecodeError:
                        pass
        elif os.path.isdir(abs_path) and not os.path.basename(abs_path).startswith('.'):
                print(f"Scanning {abs_path}")
                searchText(abs_path,fileignore_path,keyignore_path)
                path.remove(os.path.basename(abs_path))
                os.chdir('..')

            


















@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-l', '--list', is_flag=True, help='List all the guarded words')
@click.option('-inc', '--include', nargs=1, help='include a file to be scanned by removing it\'s name from  .guard/.fileignore')
def cli(ctx ,list,include):
    if ctx.invoked_subcommand is None:
        if list:
            fileignore_path = os.path.abspath(".guard/.fileignore")    #get abs path of both files 
            keyignore_path = os.path.abspath(".guard/.keyignore")       #and use in function
            file_content = load_from_files(fileignore_path,keyignore_path)
            click.echo(file_content["guarded_words"])
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

                            # lines.remove(line)  causes uninteded behaviour 
                            exempted_files.remove(line.strip("\n"))
                            click.secho(
                                f"Removed `{include}` from .fileignore", fg='green')

                    f.close()
            except FileNotFoundError:
                click.secho("Please initialize the key_guard first", fg='red')
        elif not list  and not include:
            click.secho(
                "Welcome to key_guard! Use the `--help` option for the list of options and commands available for this tool.", fg='green')










#init
@cli.command()
def init():
    '''create .guard folder and create .fileignore and .keyignore files'''
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











#scan
@cli.command()
@click.argument('path', type=click.Path(dir_okay=True), default=cwd, required=False)
def scan(path):
    '''Scan the project for any key or token'''
    fileignore_path = os.path.abspath(".guard/.fileignore")    #get abs path of both files 
    keyignore_path = os.path.abspath(".guard/.keyignore")       #and use in function
    '''Scan the project for any key or token'''
    try:
        searchText(path,fileignore_path,keyignore_path)
        click.echo(click.style("\nScanning completed successfully", fg='green'))
    except FileNotFoundError:
        click.echo(click.style("\nCould not complete scan, make sure key-guard is initialized\n", fg='red'))







#add
@cli.command()
@click.argument('add', type=str, nargs=-1 ) #add multiple words at a time
def add(add):
    '''Add new words to .guard/.keyignore'''
    guarded_words = [str(word.strip())
                         for word in open('.guard/.keyignore').readlines()]
    try:
        with open('.guard/.keyignore', 'a') as f:
            for word in add:
                if word not in guarded_words:
                    f.write(f"{word}\n")
                    click.secho(
                        f"Added `{word}` to .keyignore", fg='green')
                else:
                    click.secho(
                        f"`{word}` already exists in .guard/.keyignore", fg='yellow')
    except FileNotFoundError:
        click.secho("Please initialize the key_guard first", fg='red')
    finally:
        f.close()







#exempt
@cli.command()
@click.argument('exempt',nargs=1, type=str )
def exempt(exempt):
    '''exempt a file from scanning by adding them to .guard/.fileignore'''
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




if __name__ == '__main__':
    cli()


