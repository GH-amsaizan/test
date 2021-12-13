import click
from src.functions import create_template_env
import sys
import pathlib

SYS_PY = f"{sys.version_info.major}.{sys.version_info.minor}"
BASE_PATH = pathlib.Path.cwd()


def create_circleci(docker: bool, ecr: bool) -> None:
    """Creates circleci workflow
    
    Parameters
    ----------
    docker : bool
        Whether the user needs a docker environment or not
    ecr : bool
        Whether the user needs AWS ECR access or not

    """    
    output_path = BASE_PATH.joinpath('.circleci', 'config.yml')
    
    env = create_template_env()

    if ecr:
        template = env.get_template('config_template_ecr.yml')
    else:
        if docker:
            template = env.get_template('config_template_docker_noecr.yml')
        else:
            template = env.get_template('config_template_noecr.yml')
    
    # Render config file
    output = template.render(pyversion=SYS_PY)
    # Save rendered file to disk
    with open(output_path, 'w') as file:
        file.write(output)



@click.command()
@click.option('--docker/--no-docker', default=False, help='Whether to include a dockerfile or not, defaults to no')
@click.option('--ecr/--no-ecr', default=False, help='Whether to include connection to Amazon ECR or not, defaults to no ecr')
def cci(docker: bool, ecr: bool) -> None:
    """Creates the CircleCI workflow for the current project

    Parameters
    ----------
    docker : bool
        Whether the user needs a docker environment or not
    ecr : bool
        Whether the user needs AWS ECR access or not

    """
    # Check for missing arguments, exit if any missing
    arg_list = [True if item is None else False for item in locals().values()]
    arg_eval = sum(arg_list)
    if arg_eval > 0:
        sys.exit('Exiting setup...please provide all flags for command. Try pyrepo <command> --help to learn more.')

    click.echo('Setting up CircleCI workflow...')
    create_circleci(docker=docker, ecr=ecr)
    click.echo('CircleCI Setup Complete, see configuration in .circleci/config.yml')
