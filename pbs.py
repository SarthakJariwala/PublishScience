import click
import os
import subprocess
import github
from pbs_github import github_user
# from quick import gui_option

# @gui_option
@click.group()
def main():
    "Create a template paper folder with template files"

@main.group()
def new():
    "Create a new directory structure for publishing paper or code"

@main.group()
def get():
    "Get information for a repo"

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
    """Create a new paper dir template, options to add Code & Data folder"""
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
    """Create a new code dir template"""
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
    """Create a new data dir template"""
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

@click.option("-n", "--repo_name", type=str, help="Repository name")
@get.command()
def repo(repo_name: str):
    """Get repo by name to view traffic"""
    user = github_user()
    repos = user.get_repos()
    for repo in repos:
        name = repo.name
        if repo_name:
            if repo.name == repo_name:
                contents = repo.get_views_traffic(per="week")
                click.echo(f"{contents['views']}".format())

@click.option("-n", "--repo_name", type=str, help="Repository name")
@click.option("-d", "--desc", type=str, help="Repository description")
@click.option("-l", "--license", type=str, help="Repository license")
@new.command()
def repo(repo_name: str, desc: str, license: str):
    """Create new repository"""

    _licenses = {
        "MIT":'mit',
        "LGPL v3":"lgpl-3.0",
        "MPL v2":"mpl-2.0",
        "AGPL v3":"agpl-3.0",
        "No License":"unlicense",
        "Apache v2":"apache-2.0",
        "GPL v3":"gpl-3.0"
    }

    user = github_user()

    if not repo_name:
        repo_name = click.prompt(
            click.style(
                "Enter your repository name ", 
                fg="blue"
            ),
            type=str, default="My-pbs-created-repo"
        )
    
    if " " in repo_name:
        repo_name = repo_name.replace(" ", "-")

    description = desc if desc else github.GithubObject.NotSet

    if not license or license not in _licenses.keys():
        click.echo(
            click.style("What license would you like to use?", fg="blue")
        )
        for k,v in _licenses.items():
            click.echo(
                click.style(f"   {k}".format(), fg="blue")
            )
        
        key = click.prompt('\nEnter from above ', default="MIT")

        if key not in _licenses.keys(): # TODO ask user again if invalid
            key = "MIT"
            click.echo("Invalid selection, using MIT")
    
    click.echo(
        click.style(f"Creating new repository {repo_name}".format(), fg="blue")
    )
    
    user.create_repo(
        name=repo_name,
        description=description,
        license_template=_licenses[key],
        gitignore_template="Python"
    ) # TODO allow for other languages
    
    click.echo(click.style(f"Created {repo_name} on GitHub".format(), fg="green"))

    click.echo(click.style("Cloning to local machine", fg="blue"))

    subprocess.call(
        [f"git clone https://github.com/{user.login}/{repo_name}.git".format()], 
        shell=True
    )

    click.echo(click.style(
        "Success! Repository now available on local machine", fg="green"
        ))

@new.command()
def user():
    user = github_user()
    print(user.login)