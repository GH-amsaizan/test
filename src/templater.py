# Standard library imports
import sys
import pathlib

from configparser import ConfigParser

# Third party library imports
import click

from src.flask_app.setup_flask import flask, create_flask
from src.dash.setup_dash import dash, create_dash
from src.cicd.githubactions import create_github_actions, github_actions, lambda_workflow
from src.cicd.circleci import cci, create_circleci
from src.virtual_environment.virtual_environment import poetry, virtualenv, create_poetry, create_virtualenv
from src.postgres.postgres import postgres, create_postgres
from src.docker.docker import docker, create_docker
from src.fastapi.setup_fastapi import fastapi, create_fastapi
from src.ml.setup_ml import automl, fullml

'''
If any configuration settings are missing from a command invocation, program checks config.toml
'''

SYS_PY = f"{sys.version_info.major}.{sys.version_info.minor}"
BASE_PATH = pathlib.Path.cwd()
CONFIG_PATH = BASE_PATH.joinpath("config.toml")

# ============================================================= #
#                       CLICK COMMANDS                          #
# ============================================================= #


@click.group()
def easy() -> None:
    """
    Entry point for all easy commands
    """
    pass

extensions = [
    flask, dash, cci, lambda_workflow, github_actions, poetry, virtualenv, postgres, docker, fastapi, automl, fullml
]

for x in extensions:
    easy.add_command(x)


@click.group()
def main() -> None:
    """Setup and configure the worflows, virtual environments, and documentation of the template repo"""
    pass

# Add easy as a subgroup/subcommand under pyrepo (main)
main.add_command(easy)

@main.command()
def inspect() -> None:
    """Prints out config in config.toml
    """
    if CONFIG_PATH.exists():
        config = ConfigParser()
        config.read('config.toml')
        for item in config.items(section='main'):
            click.echo(f"{item[0].upper()} : {item[1]}")
    else:
        sys.exit('No configuration has been set...run "pyrepo easy-setup" or "pyrepo config" to set configuration')


@main.command()
@click.option('--repo', '-r', prompt='Configure template repository...\nRepository Name', help='The name of the current project')
@click.option('--describe', '-d', prompt='Repository Description', help='The name of the current project')
def easy_setup(repo: str, describe: str) -> None:
    """Quick setup of repo with basic configuration
    
    Parameters
    ----------
    repo : str
        Repository name
    describe : str
        Description of the project

    """
    click.echo('\nSetting config...')
    config = ConfigParser()
    config.add_section('main')
    config_options = [repo, describe]
    for x in config_options:
        config.set('main', str(x), str(x))

    with open(CONFIG_PATH, 'w') as f:
        config.write(f)

    click.echo('Settings saved as config.toml')
    
    req_path = BASE_PATH.joinpath('requirements.txt')

    # Set up basic github actions workflow
    create_github_actions(docker=False)

    create_virtualenv(pyversion=SYS_PY)
    
    click.echo('Basic Repository Setup Complete')


@main.command()
@click.option('--repo', '-r', prompt='Configure template repository...\nRepository Name', help='The name of the current project')
@click.option('--description', '-d', prompt='Repository Description', help='The name of the current project')
@click.option('--maintain', '-m', prompt='Maintainer', help='The name of the repository maintainer')
@click.option('--docker', is_flag=True, prompt='Docker? Deny to use virtual environment', help='Whether to include build a docker image or not, defaults to no')
@click.option('--poetry', is_flag=True, prompt='Poetry? Deny to use virtualenv', help='Whether to use poetry for virtual environment manager. If no, then virtualenv environment used.')
@click.option('--circleci', is_flag=True, prompt='CircleCI? Deny to setup GH actions', help='Whether to use CircleCI for CI/CD, defaults to no')
@click.option('--ecr', is_flag=True, prompt='Amazon ECR', help='Whether to include connection to Amazon ECR or not, defaults to no ecr')
@click.option('--flask', is_flag=True, prompt='Flask Application', help='Whether to build Flask app or not, defaults to no Flask app')
@click.option('--postgres', is_flag=True, prompt='Include Postgres with Flask', help='Whether to include Postgres database with Flask app. Defaults to no Postgres database')
@click.option('--fastapi', is_flag=True, prompt='Include FastAPI web framework', help='Whether to include fastapi web framework. Defaults to no')
@click.option('--dash-basic', is_flag=True, prompt='Do you want a basic Dash Front End?', help='Whether to include a dash front end app')
@click.option('--dash-gis', is_flag=True, prompt='Do you want a GIS specific Dash Front End?', help='Whether to include a GIS dash front end app')
def config(
    repo: str,
    description: str,
    maintain: str,
    docker: bool,
    poetry: bool,
    circleci: bool,
    ecr: bool,
    flask: bool,
    postgres: bool,
    fastapi: bool,
    dash_basic: bool,
    dash_gis: bool) -> None:
    """Set configuration values for repository setup

    Parameters
    ----------
    \n\nrepo : str - Repository name
    \n\ndescription : str - Repository description
    \n\nmaintain : str - Repository Maintainer
    \n\ndocker : bool - Whether the user needs a docker environment or not
    \n\npoetry : bool - Does the user want a poetry based virtual environment
    \n\ncircleci : bool - Does the user want a circleci workflow?
    \n\necr : bool - Whether the user needs AWS ECR access or not
    \n\nflask : bool - Does the user want a flask application?
    \n\npostgres : bool - Does the user want a postgres database included with flask?
    \n\nfastapi : bool - Does the user want a fastapi web framework?
    \n\ndash_basic : bool - Does the user want a dash front end app?
    \n\ndash_gis : bool - Does the user want a dash front end app with GIS?

    """
    # Save settings to config file, overwrites any existing config
    click.echo('\nSetting config...')
    config = ConfigParser()
    config.add_section('main')
    config_options = [repo, description, maintain, docker, poetry, circleci, ecr, flask, postgres, fastapi, dash_basic, dash_gis]
    for x in config_options:
        config.set('main', str(x), str(x))

    with open(CONFIG_PATH, 'w') as f:
        config.write(f)

    click.echo('Settings saved as config.toml')

    # Create Infrastructure
    if circleci:
        click.echo('Creating circleci pipeline')
        create_circleci(docker=docker, ecr=ecr)
    else:
        click.echo('Creating github actions workflow...')
        create_github_actions(docker=docker)

    if flask:
        click.echo('Create flask application...')
        create_flask(docker=docker)
        if postgres:
            click.echo('Adding postgres database...')
            create_postgres(pyversion=SYS_PY, docker=docker, flask=flask)
    
    if fastapi:
        click.echo('Setting up fastapi application')
        create_fastapi(docker=docker, poetry=poetry)

    if dash_basic:
        click.echo("Creating Basic Dash Front End")
        create_dash(app_type="basic", pyversion=SYS_PY, docker=docker)

    if dash_gis:
        click.echo("Creating GIS Specific Dash Front End")
        create_dash(app_type="gis", pyversion=SYS_PY, docker=docker)
    
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
    
    click.echo('Repository Setup Complete')
    click.echo('Feel free to delete templates folder')
