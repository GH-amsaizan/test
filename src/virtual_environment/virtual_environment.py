import click
from src.functions import create_template_env
import sys
import pathlib
import platform
import subprocess as sp
import os

SYS_PY = f"{sys.version_info.major}.{sys.version_info.minor}"
BASE_PATH = pathlib.Path.cwd()
CONFIG_PATH = BASE_PATH.joinpath("config.toml")


def create_env(pyversion: str, exec_path: os.PathLike) -> None:
    """Create a virtual environment in execution directory
    Parameters
    ----------
    pyversion : str
        python version used
    exec_path : pathlike object
        where to execute call command
    """

    try:
        sp.run([sys.executable, '-m', 'venv', 'env'], check=True)
    except Exception as e:
        click.echo('Error Occurred')
        click.echo(e)


def activate_and_run(command: str) -> None:
    if platform.system() == 'Linux':
        os.system(". env/bin/activate && " + command)
    elif platform.system() == 'Windows':
        os.system("cd /d env\\Scripts & activate.bat & cd /d ..\\.. & " + command)
    

def create_virtualenv(pyversion: str) -> None:
    """Set up venv virtual environment
    Parameters
    ----------
    pyversion : str
        python version used
    """
    req_path = BASE_PATH.joinpath('requirements.txt')

    # If requirements.txt exists, use it to initiate the environment
    click.echo('Creating virtual environment and installing requirements...')
    if req_path.exists():
        # Create the virtual environment
        create_env(pyversion, BASE_PATH)
      
        if platform.system() == 'Linux':
            try:
                os.system(". env/bin/activate && pip install -r requirements.txt")
                click.echo("Activate Virtual Environment with source env/bin/activate. Use deactivate to exit virtual environment")
            except Exception as e:
                sys.exit(e)
        elif platform.system() == 'Windows':
            try:
                os.system("cd /d env\\Scripts & activate.bat & cd /d ..\\.. & python -m pip install -r requirements.txt")
                click.echo("Activate Virtual Environment with .\env\Scripts\Activate.ps1 or if using command prompt use .\env\Scripts\\activate.bat. Use deactivate to exit virtual environment")
            except Exception as e:
                sys.exit(e)
        else:
            sys.exit('System not recognized, exiting setup')
    else:
        # If requirements.txt does not exist, make only a basic environment
        click.echo('No requirements.txt file detected, creating basic virtualenv environment')
        create_env(pyversion, BASE_PATH)


def create_poetry(repo: str, maintain: str, description: str) -> None:
    """Creates poetry config
    Parameters
    ----------
    repo : str
        Repository name
    maintain : str
        Repository Maintainer
    description : str
        Repository description

    """
    # Load Jinja environment and grab templates
    click.echo('Creating poetry environment...')
    
    env = create_template_env()

    template = env.get_template('pyproject_template.toml')
    # Render config file
    output = template.render(repo=repo, pyversion=SYS_PY, author=maintain, description=description)
    # Save rendered file to disk
    env_path = BASE_PATH.joinpath('pyproject.toml')
    with open(env_path, 'w') as file:
        file.write(output)

    click.echo('Poetry environment created. Add dependencies manually or use `cat requirements.txt|xargs poetry add` on Linux')





@click.command()
@click.option('--repo', '-r', help='The name of the current project')
@click.option('--maintain', '-m', help='The name of the repository maintainer')
@click.option('--description', '-d', help='Description of the repo')
def poetry(repo: str, maintain: str, description: str) -> None:
    """Creates the Poetry environment for the current project by render the pyproject.toml file based on user input,
    looks for config file if no options specified. If there are any missing arguments,
    then uses settings in config by assumption

    Parameters
    ----------
    repo : str
        Repository name
    maintain : str
        Repository Maintainer
    description : str
        Repository description
    """
    click.echo('Setting up Poetry Virtual Environment Configuration...')
    arg_list = [True if item is None else False for item in locals().values()]
    arg_eval = sum(arg_list)
    # Check for missing arguments, exit if any missing
    if arg_eval > 0:
        sys.exit('Exiting setup...please provide all flags for command. Try pyrepo <command> --help to learn more.')
    
    create_poetry(repo=repo, maintain=maintain, description=description)
    click.echo('Poetry Setup Complete, see configuration in pyproject.toml')


@click.command()
def virtualenv() -> None:
    """Creates the venv virtual environment for the current project

    Parameters
    ----------
    N/A
    """
    click.echo('Setting up Virtualenv Virtual Environment Configuration...')
 
    create_virtualenv(pyversion=SYS_PY)
    click.echo('Setup of virtual environment complete, environment located in ./env folder')