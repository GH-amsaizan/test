import click
from src.functions import create_template_env
import sys
import pathlib

SYS_PY = f"{sys.version_info.major}.{sys.version_info.minor}"
BASE_PATH = pathlib.Path.cwd()


def create_docker(pyversion: str) -> None:
    """Create a Dockerfile
    
    Parameters
    ----------
    pyversion : str
        python version used

    """
    click.echo('Creating Dockerfile...')
    output_path = BASE_PATH

    env = create_template_env()

    docker_files = ['Dockerfile_proj','.dockerignore']
    for x in docker_files:
        template = env.get_template(x)
        # Render config file
        output = template.render(pyversion=pyversion)

        if x =='Dockerfile_proj':
            x = 'Dockerfile'
        # Save rendered file to disk
        with open(output_path.joinpath(x), 'w') as file:
            file.write(output)
    click.echo('Dockerfile has been integrated. See configuration in ./Dockerfile. Reference .dockerignore for files to exclude from the build image.')


@click.command()
def docker() -> None:
    """Easy setup of docker with standard Dockerfile

    Parameters
    ----------
    N/A

    """
    create_docker(pyversion=SYS_PY)
    click.echo('Dockerfile has been integrated. See configuration in ./Dockerfile. Reference .dockerignore for files to exclude from the build image.')