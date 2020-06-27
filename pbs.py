import click
import os
# from quick import gui_option

# @gui_option
@click.group()
def main():
    "Create a template paper folder with template files"

@main.group()
def new():
    "Create a new directory structure for publishing paper or code"

def _create_paper_directory(name):
    if name:
        path = os.path.join(os.getcwd(), name)
        try:
            os.mkdir(path)
        except OSError:
            click.echo(f'Can not access {path}'.format())
            click.echo('Check if folder name already exists OR')
            click.echo('Check if you have access to modify this folder')
            path = None
        return path

def _create_code_directory(name, path=None):
    if name:
        if path is None:
            path = os.path.join(os.getcwd(), name)
        else:
            path = os.path.join(path, name)
        
        try:
            os.mkdir(path)
        except OSError:
            click.echo(f'Can not access {path}'.format())
            click.echo('Check if folder name already exists OR')
            click.echo('Check if you have access to modify this folder')
            path = None
        
        return path

def _create_data_directory(name, path=None):#Redundant
    if name:
        if path is None:
            path = os.path.join(os.getcwd(), name)
        else:
            path = os.path.join(path, name)
        
        try:
            os.mkdir(path)
        except OSError:
            click.echo(f'Can not access {path}'.format())
            click.echo('Check if folder name already exists OR')
            click.echo('Check if you have access to modify this folder')
            path = None
        
        return path

@click.option('-n', '--name', type=str, help='Name of your paper/folder')
@click.option('-c', '--code', type=bool, help='Create a folder for code')
@click.option('-d', '--data', type=bool, help='Create a folder for data')
@new.command()
def paper(name: str, code: bool, data: bool):
    """Create a new paper directory template, with options to create a Code and Data folder"""
    if not name:
        click.echo("No paper name provided")
        name = click.prompt(
            "Please enter a name (Default: MyAwesomePaper)", 
            type=str,
            default="MyAwesomePaper"
        )
        
    path = _create_paper_directory(name)
    if path:
        click.echo(
            f"New directory {name} created in ".format() + 
            click.style(f"{path}".format(), fg="blue")
        )
    
        if code:
            code_path = _create_code_directory("Code", path=path)
            if code_path:
                click.echo(f"You can store your code in {code_path}".format())
        
        if data:
            data_path = _create_data_directory("Data", path=path)
            if code_path:
                click.echo(f"You can store your data in {data_path}".format())

@click.option("-n", "--name", type=str, help="Create a new code directory")
@new.command()
def code(name: str):
    if not name:
        click.echo("No name provided")
        name = click.prompt(
            "Please enter a name (Default: MyAwesomeCode)", 
            type=str,
            default="MyAwesomeCode"
        )
    
    path = _create_code_directory(name)
    if path:
        click.echo(f"New code directory {path} created".format())

@click.option("-n", "--name", type=str, help="Create a new data directory")
@new.command()
def data(name: str):
    if not name:
        click.echo("No name provided")
        name = click.prompt(
            "Please enter a name (Default: MyAwesomeData)", 
            type=str,
            default="MyAwesomeData"
        )
    
    path = _create_data_directory(name)
    if path:
        click.echo(f"New data directory {path} created".format())