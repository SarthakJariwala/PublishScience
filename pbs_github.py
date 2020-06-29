import click
import subprocess
import os
import sys
import github
from github import Github
# from dotenv import load_dotenv

def github_user():
    # load_dotenv()
    try:
        username = os.environ['PBS_GITHUB_USERNAME']
        password = os.environ['PBS_GITHUB_PASSWORD']
    except:
        username = click.prompt(
            click.style("GitHub Username ", fg='blue')
            )
        password = click.prompt(
            click.style("GitHub Password ", fg='blue'),
            hide_input=True)
        
        # TODO set it to env vars from pbs
        # ans = click.prompt(
        #     click.style(
        #         "Save username and password for this computer?\n"+
        #         "(Only recommended for personal computer)",
        #         fg="green"
        #     ),
        #     default="Yes"
        # )

        # if ans == "Yes":
        #     if sys.platform == "darwin":
        #         subprocess.call(
        #             [f"export PBS_GITHUB_USERNAME={username}".format()],
        #             shell=True
        #         )
        #         subprocess.call(
        #             [f"export PBS_GITHUB_PASSWORD={password}".format()],
        #             shell=True
        #         )
        #         print('worked')
        #     # os.putenv('PBS_GITHUB_USERNAME', username)
        #     # os.putenv('PBS_GITHUB_PASSWORD', password)

        #     print("Now fetching username")
        #     # print(os.environ['PBS_GITHUB_USERNAME'])
        #     subprocess.call(
        #             ["echo $PBS_GITHUB_USERNAME"],
        #             shell=True
        #         )

    if username and password:
        try:
            g = Github(username, password)
            user = g.get_user()
            
        except: # TODO catch exception
            click.echo(click.style("Credentials not valid", fg="red"))
            github_user()
        
        return user

def select_license(license: str):
    _licenses = {
        "1":'mit',
        "2":"lgpl-3.0",
        "3":"mpl-2.0",
        "4":"agpl-3.0",
        "5":"apache-2.0",
        "6":"gpl-3.0",
        "7":"unlicense",
        "8":"no license" #github.GithubObject.NotSet
    }

    if not license or license not in _licenses.keys() or license not in _licenses.values():
        click.echo(
            click.style("What license would you like to use?", fg="blue")
        )
        for k,v in _licenses.items():
            click.echo(
                click.style(f"   {k} : {v.upper()}".format(), fg="blue")
            )
        
        key = click.prompt('\nEnter a number from above ', default="8")

        if key not in _licenses.keys(): # TODO ask user again if invalid
            click.echo(click.style("Invalid selection! Setting no license", fg="red"))
            key = "8"
        
        if key == "8":
            selected_license = github.GithubObject.NotSet
        else:
            selected_license = _licenses[key]
        
        return selected_license
    
    else:
        return license