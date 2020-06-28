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