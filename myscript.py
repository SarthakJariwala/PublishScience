import click
# from quick import gui_option

# @gui_option
@click.group()
def main():
    "Create a template paper folder with template files"

@click.option('-n', '--name', type=str, help='Name of the folder')
@click.option('-c', '--code', type=bool, help='Create a folder for code')
@click.option('-d', '--data', type=bool, help='Create a folder for data')
@main.command()
def create(name: str, code: bool, data: bool):
    "Create a new directory structure for the paper"
    if name:
        click.echo(f"New directory {name} created".format(name))
        if code:
            click.echo(f"You can store your code in /{name}/Code".format(name))
        if data:
            click.echo(f"You can store your data in /{name}/Data".format(name))
    # if name and code:
    #     click.echo(f"New directory {name} with 'Code' folder created.".format(name))
    elif not name:
        click.echo("No paper name provided. Try again with 'pbs create -n YOUR_PAPER_NAME' ")