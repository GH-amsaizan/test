import click
import sys
import pathlib
import subprocess as sp
import os

from src.docker.docker import create_docker
from src.functions import squash_requirement_files, create_template_env
from src.virtual_environment.virtual_environment import create_poetry, create_virtualenv

SYS_PY = f"{sys.version_info.major}.{sys.version_info.minor}"
BASE_PATH = pathlib.Path.cwd()

env = create_template_env()

def create_dash(app_type: str, docker: bool, pyversion: str  = SYS_PY) -> None:
    """Create GIS based Dash App
    
    Parameters
    ----------
    app_type: str
        Specific type of dash application to create
    docker : bool
        Whether the user needs a docker environment or not
    pyversion : str
        Python version used

    """
    os.makedirs(f"dash-{app_type}", exist_ok=True)
    output_path = BASE_PATH.joinpath(f"dash-{app_type}")

    dash_files = [f"dash_{app_type}_requirements.txt", f"dash_{app_type}_template.py"]

    # Render config file and save rendered file to disk
    for x in dash_files:
        if x.endswith('.txt'):
            output = squash_requirement_files(x)
            with open(BASE_PATH.joinpath('requirements.txt'), "w") as file:
                file.write(output)
        else:
            template = env.get_template(x)
            output = template.render(pyversion=pyversion)
            with open(output_path.joinpath(x), "w") as file:
                file.write(output)



@click.command()
@click.option('--repo', '-r', prompt='Configure template repository...\nRepository Name', help='The name of the current project')
@click.option('--describe', '-d', prompt='Repository Description', help='The name of the current project')
@click.option('--maintain', '-m', prompt='Maintainer', help='The name of the repository maintainer')
@click.option("--docker", default=False, is_flag=True, help="Whether to include build a docker image or not, defaults to no")
@click.option("--basic", "app_type", flag_value="basic", help="Whether to include a general dash front end app")
@click.option("--gis", "app_type", flag_value="gis", help="Whether to include a GIS specific dash front end app")
@click.option('--docker', is_flag=True, prompt='Docker? Deny to use virtual environment', help='Whether to include build a docker image or not, defaults to no')
@click.option('--poetry', is_flag=True, prompt='Poetry? Deny to use virtualenv', help='Whether to use poetry for virtual environment manager. If no, then virtualenv environment used.')
def dash(repo: str, maintain: str, describe: str, docker: bool, poetry: bool, app_type: str = "basic") -> None:
    """Creates a bare bones Dash Application

    Parameters
    ----------
    repo : str
        Repository name
    maintain : str
        Repository Maintainer
    describe : str
        Repository description
    docker : bool
        Whether the user needs a docker environment or not
    poetry : bool
        Whether the user needs a poetry environment or not
    app_type : str
        Specific type of dash application to create

    """
    # Check for missing arguments, exit if any missing
    arg_list = [True if item is None else False for item in locals().values()]
    arg_eval = sum(arg_list)

    if arg_eval > 0:
        sys.exit('Exiting setup...please provide all flags for command. Try pyrepo <command> --help to learn more.')
    
    click.echo(f"Importing {app_type} Dash files...")
    
    create_dash(app_type=app_type, pyversion=SYS_PY, docker=docker)
    click.echo(f"Dash files have been setup. Run Python dash-{app_type}/dash_{app_type}_template.py to launch server")

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