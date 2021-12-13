import click
import sys
from os import PathLike
import pathlib
import shutil

from src.cicd.githubactions import create_github_actions
from src.docker.docker import create_docker
from src.functions import squash_requirement_files, create_template_env
from src.virtual_environment.virtual_environment import create_poetry, create_virtualenv

SYS_PY = f"{sys.version_info.major}.{sys.version_info.minor}"
BASE_PATH = pathlib.Path.cwd()


def create_fastapi(docker: bool, poetry: bool) -> None:
    """Create Fastapi app
    
    Parameters
    ----------
    docker : bool
        Whether the user needs a docker environment or not
    poetry: bool
        Whether the user needs a poetry environment or not

    """
    n = BASE_PATH.joinpath(pathlib.Path('fastapi'))
    n.mkdir(parents=True, exist_ok=True)
    output_path = BASE_PATH.joinpath('fastapi')
    
    env = create_template_env()

    fastapi_files = ['fastapi_requirements.txt','fastapi_app.py', 'fastapi_models.py', 'fastapi_database.py']
    for x in fastapi_files:
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

    # MyPy throws error if the following operation is placed inside of a loop for DRY
    item = BASE_PATH.joinpath('templates', pathlib.Path("fastapi_layout.html"))
    copy = output_path.joinpath(pathlib.Path("fastapi_layout.html"))
    shutil.copyfile(item, copy)
    item = BASE_PATH.joinpath('templates', pathlib.Path("fastapi_home.html"))
    copy = output_path.joinpath(pathlib.Path("fastapi_home.html"))
    shutil.copyfile(item, copy)



@click.command()
@click.option('--repo', '-r', prompt='Configure template repository...\nRepository Name', help='The name of the current project')
@click.option('--describe', '-d', prompt='Repository Description', help='The name of the current project')
@click.option('--maintain', '-m', prompt='Maintainer', help='The name of the repository maintainer')
@click.option('--docker', is_flag=True, prompt='Docker? Deny to use virtual environment', help='Whether to include build a docker image or not, defaults to no')
@click.option('--poetry', is_flag=True, prompt='Poetry? Deny to use virtualenv', help='Whether to use poetry for virtual environment manager. If no, then virtualenv environment used.')
def fastapi(repo: str, describe: str, maintain: str, docker: bool, poetry: bool) -> None:
    """
    Create a FastAPI app with full CRUD functionality
    
    Parameters
    ----------
    repo : str
        Repository name
    describe : str
        Description of the project
    maintain : str
        Repository Maintainer
    docker : bool
        Whether the user needs a docker environment or not
    poetry : bool
        Whether the user needs a poetry environment or not

    """
    arg_list = [True if item is None else False for item in locals().values()]
    arg_eval = sum(arg_list)
    # Check for missing arguments, exit if any missing
    if arg_eval > 0:
        sys.exit('Exiting setup...please provide all flags for command. Try pyrepo <command> --help to learn more.')
    
    req_path = BASE_PATH.joinpath('requirements.txt')

    create_github_actions(docker=True)
    print('Github actions created')

    create_fastapi(docker=True, poetry=False)
    print('Navigate to and run fastapi/fastapi_app.py to start your app')

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