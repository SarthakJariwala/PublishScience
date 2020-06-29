import click
from pyscaffold.api import create_project

def new_python_project(name: str, author: str): 
    if name is None:
        name = click.prompt(
            click.style("Enter your python project name ", fg='blue'),
            default="My PyProject"
        )
    
    if author is None:
        author = click.prompt(
            click.style("Enter project authors ", fg='blue')
        )

    create_project(
        project=name, author=author,
        license="mit"
    )
