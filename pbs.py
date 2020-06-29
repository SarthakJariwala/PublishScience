import click
import os
import subprocess
import git
import github
from pbs_github import github_user, select_license
from pbs_python import new_python_project
from utils import changedir
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
    """Create new repository on GitHub"""

    user = github_user()

    if not repo_name:
        repo_name = click.prompt(
            click.style(
                "Enter your repository name ", 
                fg="blue"
            ),
            type=str, default="New PBS Project"
        )
    
    if " " in repo_name:
        repo_name = repo_name.replace(" ", "-")
    
    if not desc:
        description = click.prompt(
            click.style(f"Add description for {repo_name}".format(), fg='blue'),
            default=f"Description for {repo_name}".format()
        )
    else:
        description = desc

    selected_license = select_license(license)
    
    click.echo(
        click.style(f"Creating new repository {repo_name} on GitHub".format(), fg="blue")
    )
    
    user.create_repo(
        name=repo_name,
        description=description,
        license_template=selected_license,
        gitignore_template="Python"
    ) # TODO allow for other languages
    
    click.echo(click.style(f"Created {repo_name} on GitHub".format(), fg="green"))

    click.echo(click.style(f"Cloning {repo_name} to local machine".format(), fg="blue"))

    g = git.cmd.Git(os.getcwd())
    g.execute(["git", "clone", f"https://github.com/{user.login}/{repo_name}.git".format()])

    click.echo(click.style(
        f"Success! {repo_name} now available on local machine".format(), fg="green"
        ))
    
    # ans = click.prompt(
    #     click.style(
    #         f"Do you want to create a Python project template for {repo_name}?".format(), 
    #         fg="blue"),
    #     type=click.Choice(['y','n'], case_sensitive=False), 
    #     show_choices=True, default='n'
    # )

    # if ans.lower() == 'y':
    #     with changedir(f"{repo_name}".format()):
    #         new_python_project(repo_name, None)
    #         click.echo(click.style("Python project created!", fg='green'))

    #         ans = click.prompt(
    #             click.style("Push additions to GitHub?", fg="blue"),
    #             type=click.Choice(['y','n'], case_sensitive=False), 
    #             show_choices=True, default='n')

        
        # if ans.lower() == 'y':


@click.option('-n', '--name', type=str, help="python project name")
@click.option('-a', '--author', type=str, help="project author names")
@new.command()
def pyproject(name: str, author: str):
    """Create new structured python project with template""" 
    new_python_project(name, author)

@main.command()
def user():
    "Shows GitHub user"
    user = github_user()
    print(user.login)