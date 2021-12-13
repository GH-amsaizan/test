import click
from src.functions import create_template_env
import sys
import pathlib
import shutil


SYS_PY = f"{sys.version_info.major}.{sys.version_info.minor}"
BASE_PATH = pathlib.Path.cwd()


def create_github_actions(docker: bool) -> None:
    """Create a github actions workflow
    
    Parameters
    ----------
    docker : bool
        User requires a docker environment

    """
    master_path = BASE_PATH.joinpath('.github', 'workflows', 'workflow_master.yml')
    dev_path = BASE_PATH.joinpath('.github', 'workflows', 'workflow_dev.yml')

    env = create_template_env()
    
    if docker:
        template_master = env.get_template('workflow_master_template_docker.yml')
        template_dev = env.get_template('workflow_dev_template_docker.yml')
    else:
        template_master = env.get_template('workflow_master_template_nodocker.yml')
        template_dev = env.get_template('workflow_dev_template_nodocker.yml')
    
    # Render files, and within them render Github related secrets as Jinja will try to render them and throw an error
    output_master = template_master.render(pyversion=SYS_PY,  codecov='${{ secrets.CODECOV_TOKEN }}', github='${{ secrets.GITHUB_TOKEN }}')
    output_dev = template_dev.render(pyversion=SYS_PY,  codecov='${{ secrets.CODECOV_TOKEN }}', github='${{ secrets.GITHUB_TOKEN }}')

    # Save rendered file to disk
    with open(master_path, 'w') as file:
        file.write(output_master)
    with open(dev_path, 'w') as file:
        file.write(output_dev)
    

@click.command()
@click.option('--docker/--no-docker', default=False, help='Whether to include build a docker image or not, defaults to no')
def github_actions(docker: bool) -> None:
    """Creates the Github Actions workflow for the current project by rendering the worflow.yml files based on user input

    Parameters
    ----------
    docker : bool
        Whether the user needs a docker environment or not

    """
    click.echo('Setting up Github Actions workflow...')
    create_github_actions(docker=docker)
    click.echo('Github Actions Setup Complete, see configuration in .github/workflows/workflow_*.yml')



@click.command()
def lambda_workflow() -> None:
    """Creates a Lambda Github actions workflow for the current project
    """
    click.echo('Setting up Lambda workflow...')
    path_in = BASE_PATH.joinpath('templates', 'lambda_template.yml')
    path_out = BASE_PATH.joinpath('.github', 'workflows', 'lambda.yml')
    shutil.copyfile(path_in, path_out)
    click.echo('Lambda Setup Complete, see configuration in .github/workflows/lambda.yml')