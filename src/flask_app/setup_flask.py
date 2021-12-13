import click
import sys
import pathlib
import os

from src.cicd.githubactions import create_github_actions
from src.docker.docker import create_docker
from src.functions import squash_requirement_files, create_template_env
from src.virtual_environment.virtual_environment import create_poetry, create_virtualenv


SYS_PY = f"{sys.version_info.major}.{sys.version_info.minor}"
BASE_PATH = pathlib.Path.cwd()


def create_flask(docker: bool) -> None:
    """Create Flask App
    
    Parameters
    ----------
    docker : bool
        Whether the user needs a docker environment or not

    """
    os.makedirs('flask', exist_ok=True)
    output_path = BASE_PATH.joinpath('flask')

    env = create_template_env()
    
    flask_files = ['flask_app.py', 'flask_requirements.txt']
    for x in flask_files:
        if x.endswith('.txt'):
            output = squash_requirement_files(x)
            with open(BASE_PATH.joinpath('requirements.txt'), "w") as file:
                file.write(output)
        else:
            template = env.get_template(x)
            # Render config file
            output = template.render(pyversion=SYS_PY)
            # Save rendered file to disk
            with open(output_path.joinpath(x), 'w') as file:
                file.write(output)


        

@click.command()
@click.option('--repo', '-r', prompt='Configure template repository...\nRepository Name', help='The name of the current project')
@click.option('--describe', '-d', prompt='Repository Description', help='The name of the current project')
@click.option('--maintain', '-m', prompt='Maintainer', help='The name of the repository maintainer')
@click.option('--docker', is_flag=True, prompt='Docker? Deny to use virtual environment', help='Whether to include build a docker image or not, defaults to no')
@click.option('--poetry', is_flag=True, prompt='Poetry? Deny to use virtualenv', help='Whether to use poetry for virtual environment manager. If no, then virtualenv environment used.')
def flask(repo: str, describe: str, maintain: str, docker: bool, poetry: bool) -> None:
    """
    Easy setup of flask repo with basic configuration

    Parameters
    ----------
    repo : str
        Repository name
    describe : str
        Description of the project
    maintain : str
        Repository Maintainer
    docker : bool
        Whether to include a Dockerfile or not
    poetry : bool
        Does the user want a poetry based virtual environment

    """
    arg_list = [True if item is None else False for item in locals().values()]
    arg_eval = sum(arg_list)
    # Check for missing arguments, exit if any missing
    if arg_eval > 0:
        sys.exit('Exiting setup...please provide all flags for command. Try pyrepo <command> --help to learn more.')
    
    req_path = BASE_PATH.joinpath('requirements.txt')

    create_github_actions(docker=True)
    print('Github actions created')

    create_flask(docker=True)
    click.echo('Flask Application setup is complete. See configuration in flask/app.py')

    if docker:
        create_docker(pyversion=SYS_PY)
        click.echo('Dockerfile has been integrated. See configuration in ./Dockerfile. Reference .dockerignore for files to exclude from the build image.')
    elif poetry:
        click.echo('Creating poetry environment')
        create_poetry(repo=repo, maintain=maintain, description=describe)
    else:
        click.echo('Creating virtual env')
        # Keep virtual environment config at the end of this list of if/else statements to
        # install the latest requirements.txt into the virtual environment
        create_virtualenv(pyversion=SYS_PY)
 
