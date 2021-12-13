import click
import sys
import pathlib
import os

from src.docker.docker import create_docker
from src.functions import squash_requirement_files, create_template_env
from src.virtual_environment.virtual_environment import create_poetry, create_virtualenv, activate_and_run

SYS_PY = f"{sys.version_info.major}.{sys.version_info.minor}"
BASE_PATH = pathlib.Path.cwd()

env = create_template_env()

def create_automl() -> None:
    """Auto ML Implementation
    
    Parameters
    ----------
    None

    """
    click.echo('Creating AutoML Implementation...')
    os.makedirs("ml", exist_ok=True)
    output_path = BASE_PATH.joinpath("ml")
   
    automl_files = ["automl.py", "automl_requirements.txt"]

    # Render config file and save rendered file to disk
    for f in automl_files:
        if f.endswith('.txt'):
            output = squash_requirement_files(f)
            with open(BASE_PATH.joinpath('requirements.txt'), "w") as file:
                file.write(output)
        else:
            template = env.get_template(f)
            output = template.render(pyversion=SYS_PY)
            with open(output_path.joinpath(f), "w") as file:
                file.write(output)
    click.echo("AutoML Implementation created. See ml/ directory to begin.")


def create_fullml() -> None:
    """Full ML Implementation
    
    Parameters
    ----------
    None

    """
    click.echo('Creating Full ML Pipeline Implementation...')
    os.makedirs("ml", exist_ok=True)
    output_path = BASE_PATH.joinpath("ml")
   
    fullml_files = ["ingest.py", "clean.py", "validate.py", "profile.py", "model.py", "dvc.yaml", "params.yaml", "fullml_requirements.txt"]

    # Render config file and save rendered file to disk
    for f in fullml_files:
        if f.endswith('.txt'):
            output = squash_requirement_files(f)
            with open(BASE_PATH.joinpath('requirements.txt'), "w") as file:
                file.write(output)
        else:
            template = env.get_template(f)
            output = template.render(pyversion=SYS_PY)
            with open(output_path.joinpath(f), "w") as file:
                file.write(output)
    
   


@click.command()
@click.option('--docker', default=False, is_flag=True, prompt='Docker? Deny to use virtual environment', help='Whether to include build a docker image or not, defaults to no')
@click.option('--poetry', default=False, is_flag=True, prompt='Poetry? Deny to use virtualenv', help='Whether to use poetry for virtual environment manager. If no, then virtualenv environment used.')
@click.option('--repo', '-r', prompt='Configure template repository...\nRepository Name', help='The name of the current project')
@click.option('--describe', '-d', prompt='Repository Description', help='The name of the current project')
@click.option('--maintain', '-m', prompt='Maintainer', help='The name of the repository maintainer')
def automl(docker: bool, poetry: bool, repo: str, describe: str, maintain: str) -> None:
    """Creates a basic automl pipeline implementation using mljar-supervised

    Parameters
    ----------
    docker : bool
        Whether the user needs a docker environment or not
    poetry : bool
        Whether the user wants to use poetry for VE
    repo : str
        Repo name
    describe : str
        Repo Description
    maintainer: str
        Repo Maintainer

    """
    # Check for missing arguments, exit if missing according to criteria
    if poetry:
        arg_list = [True if item is None else False for item in locals().values()]
        arg_eval = sum(arg_list)
        # Expect all arguments if poetry selected
        if arg_eval > 0:
            sys.exit('Exiting setup...please provide all flags for command. Try pyrepo <command> --help to learn more.')
    
    # Create AutoML
    create_automl()

    # Environment/Dependency Management
    if docker:
        create_docker(pyversion=SYS_PY)
    elif poetry:
        create_poetry(repo=repo, maintain=maintain, description=describe)
    else:
        create_virtualenv(pyversion=SYS_PY)


@click.command()
@click.option('--docker', default=False, is_flag=True, prompt='Docker? Deny to use virtual environment', help='Whether to include build a docker image or not, defaults to no')
@click.option('--poetry', default=False, is_flag=True, prompt='Poetry? Deny to use virtualenv', help='Whether to use poetry for virtual environment manager. If no, then virtualenv environment used.')
@click.option('--repo', '-r', prompt='Configure template repository...\nRepository Name', help='The name of the current project')
@click.option('--describe', '-d', prompt='Repository Description', help='The name of the current project')
@click.option('--maintain', '-m', prompt='Maintainer', help='The name of the repository maintainer')
def fullml(docker: bool, poetry: bool, repo: str, describe: str, maintain: str) -> None:
    """Creates a full ml pipeline with DVC and MLFlow installed

    Parameters
    ----------
    docker : bool
        Whether the user needs a docker environment or not
    poetry : bool
        Whether the user wants to use poetry for VE
    repo : str
        Repo name
    describe : str
        Repo Description
    maintainer: str
        Repo Maintainer

    """
    # Check for missing arguments, exit if missing according to criteria
    if poetry:
        arg_list = [True if item is None else False for item in locals().values()]
        arg_eval = sum(arg_list)
        # Expect all arguments if poetry selected
        if arg_eval > 0:
            sys.exit('Exiting setup...please provide all flags for command. Try pyrepo <command> --help to learn more.')
    
    # Create Full ML Pipeline
    create_fullml()

    # Environment/Dependency Management
    if docker:
        create_docker(pyversion=SYS_PY)
    elif poetry:
        create_poetry(repo=repo, maintain=maintain, description=describe)
    else:
        create_virtualenv(pyversion=SYS_PY)
    
    # Delete dvc.yaml so doesn't clutter dvc init
    BASE_PATH.joinpath('templates', 'dvc.yaml').unlink()
    
    # Make new directories to hold data artifacts
    data_path = BASE_PATH.joinpath('ml', 'data')
    data_path.mkdir(exist_ok=True)
    new_paths = ['raw', 'processed', 'results', 'external', 'profile_reports']
    for path in new_paths:
        data_path.joinpath(path).mkdir(exist_ok=True)
    
    # Activate VE and run dvc init
    activate_and_run('dvc init')

    click.echo("Full ML Implementation created. See ml directory or run `dvc status` to begin.")
    click.echo("Visit the README for more in depth information on how to use the full ML use case")

