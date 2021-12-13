import click
import sys
import pathlib

from src.flask_app.setup_flask import create_flask
from src.functions import squash_requirement_files, create_template_env
from src.virtual_environment.virtual_environment import create_poetry, create_virtualenv
from src.docker.docker import create_docker

SYS_PY = f"{sys.version_info.major}.{sys.version_info.minor}"
BASE_PATH = pathlib.Path.cwd()


def create_postgres(pyversion: str, docker: bool, flask: bool) -> None:
    """Create Flask App w/ Postgres Database
    
    Parameters
    ----------
    pyversion : str
        python version used
    docker : bool
        Whether the user needs a docker environment or not
    flask : bool
        Does the user want a flask application?

    """
    output_path = BASE_PATH.joinpath('flask')
    
    env = create_template_env()

    flask_postgres_files = ['flask_postgres_README.md','flask_postgres_requirements.txt','flask_postgres.py']
    for x in flask_postgres_files:
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
@click.option('--description', '-d', prompt='Repository Description', help='The name of the current project')
@click.option('--maintain', '-m', prompt='Maintainer', help='The name of the repository maintainer')
@click.option('--docker', is_flag=True, prompt='Docker? Deny to use virtual environment', help='Whether to include build a docker image or not, defaults to no')
@click.option('--poetry', is_flag=True, prompt='Poetry? Deny to use virtualenv', help='Whether to use poetry for virtual environment manager. If no, then virtualenv environment used.')
@click.option('--flask/--no-flask', default=False, prompt='Flask Application', help='Whether to build Flask app or not, defaults to no Flask app')
def postgres(repo: str, description: str, maintain: str, docker: bool, flask: bool, poetry: bool) -> None:
    """Creates the Postgres Integration with Flask

    Parameters
    ----------
    repo : str
        Repo Name
    description : str
        Repo Description
    maintain : str
        Repo Maintainer
    docker : bool
        Whether the user needs a docker environment or not
    flask : bool
        Does the user want a flask application?
    poetry : bool
        Does the user want a poetry based virtual environment

    """
    arg_list = [True if item is None else False for item in locals().values()]
    arg_eval = sum(arg_list)
    # Check for missing arguments, exit if any missing
    if arg_eval > 0:
        sys.exit('Exiting setup...please provide all flags for command. Try pyrepo <command> --help to learn more.')

    if flask == False:
        sys.exit('This configuration requires a flask application to exist, please enable flask to integrate postgres database.')

    create_flask(docker=True)
    click.echo('Flask Application setup is complete. See configuration in flask/app.py')
    
    click.echo('Creating Postgres files...')
    create_postgres(pyversion=SYS_PY, docker=docker, flask=flask)
    click.echo('Postgres integration files have been setup. Please see flask_postgres_README.md for instructions on how to set up Postgres credentials and DB tables via CLI.')

    if docker:
        click.echo('You have decided to use Docker')
        create_docker(pyversion=SYS_PY)
    elif poetry:
        click.echo('Creating poetry environment')
        create_poetry(repo=repo, maintain=maintain, description=description)
    else:
        click.echo('Creating virtual env')
        # Keep virtual environment config at the end of this list of if/else statements to
        # install the latest requirements.txt into the virtual environment
        create_virtualenv(pyversion=SYS_PY)