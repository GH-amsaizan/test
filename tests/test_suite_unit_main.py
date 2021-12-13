import pytest
import pathlib
from configparser import ConfigParser
import platform
import os
import sys

from src.flask_app.setup_flask import create_flask
from src.dash.setup_dash import create_dash
from src.cicd.githubactions import create_github_actions
from src.cicd.circleci import create_circleci
from src.virtual_environment.virtual_environment import create_poetry, create_virtualenv, create_env
from src.postgres.postgres import create_postgres
from src.docker.docker import create_docker
from src.templater import easy_setup
from src.fastapi.setup_fastapi import create_fastapi
from src.ml.setup_ml import create_automl, create_fullml

# pytest sets cwd as the repository root
root_path = pathlib.Path().cwd()

SYS_PY = f"{sys.version_info.major}.{sys.version_info.minor}"

def test_root_structure():
    # Ensure all root folders are present
    folder_list = ['.github', '.circleci', 'docs', 'src', 'tests', 'templates']
    for folder in folder_list:
        new_path = root_path.joinpath(folder)
        assert new_path.is_dir()


def test_create_github_actions():
    # Test create_github_actions function
    docker = True

    create_github_actions(docker)
    workflow_master_path = root_path.joinpath('.github', 'workflows', 'workflow_master.yml')
    workflow_dev_path = root_path.joinpath('.github', 'workflows', 'workflow_dev.yml')

    assert workflow_master_path.is_file()
    assert workflow_dev_path.is_file()


def test_create_virtualenv():
    # Test create_virtualenv function
    pyversion = '3.8'

    # Make requirements.txt file
    req_text_list = ['scikit-learn', 'numpy', 'cerberus']
    with open('requirements.txt', 'w') as file:
        file.write('\n'.join(req_text_list))

    create_virtualenv(pyversion)
    
    # Check that reqs were installed in virtual environment
    if platform.system() == 'Linux':
        os.system(". env/bin/activate && pip freeze > check_reqs.txt")
    elif platform.system() == 'Windows':
        os.system("cd /d env\\Scripts & activate.bat & cd /d ..\\.. & python -m pip freeze > check_reqs.txt")
    else:
        assert False
    
    with open('check_reqs.txt', 'r') as f:
        req_check_list = f.readlines()
        req_check_list = [item.replace('\n', '') for item in req_check_list]
        req_check_list = [item.split('==')[0] for item in req_check_list]
    
    for req in req_text_list:
        print(f'req {req}')
        print(f'req_check_list {req_check_list}')
        checklist = [True if req in item.lower() else False for item in req_check_list]
        assert sum(checklist) >= 1


def test_create_flask():
    # Test create_flask function
    docker = False

    create_flask(docker)

    flask_app_dir = root_path.joinpath('flask')
    flask_app_path = root_path.joinpath('flask', 'flask_app.py')

    assert flask_app_dir.is_dir()
    assert flask_app_path.is_file()


def test_create_dash_basic():
    # Test create_dash function
    app_type = 'basic'
    pyversion = '3.8'
    docker = False
    create_dash(app_type, pyversion, docker)

    dash_files = ["dash_basic_template.py"]

    assert root_path.joinpath('dash-basic').is_dir()

    for file in dash_files:
        file_path = root_path.joinpath('dash-basic', file)
        assert file_path.is_file()


def test_create_dash_gis():
    # Test create_dash function
    app_type = 'gis'
    pyversion = '3.8'
    docker = False
    create_dash(app_type, pyversion, docker)

    dash_files = ["dash_gis_template.py"]

    assert root_path.joinpath('dash-gis').is_dir()

    for file in dash_files:
        file_path = root_path.joinpath('dash-gis', file)
        assert file_path.is_file()


def test_create_circleci():
    # Test create_circleci function
    docker = True
    ecr = True

    create_circleci(docker, ecr)
    config_path = root_path.joinpath('.circleci', 'config.yml')

    assert config_path.is_file()


def test_create_poetry():
    # Test create_poetry function
    repo = 'Test-Repo-5000'
    maintain = 'Rando McGee'
    description = 'An inevitable failure'
    create_poetry(repo, maintain, description)
    
    pyproj_path = root_path.joinpath('pyproject.toml')
    config = ConfigParser()
    config.read('pyproject.toml')

    assert pyproj_path.is_file()
    assert config.has_section('tool.poetry')
    assert config.has_section('tool.poetry.dependencies')

    assert config.get('tool.poetry', 'name') == '"Test-Repo-5000"'
    assert config.get('tool.poetry.dependencies', 'python') == f'"{SYS_PY}"'
    assert config.get('tool.poetry', 'authors') == '["Rando McGee"]'
    assert config.get('tool.poetry', 'description') == '"An inevitable failure"'


def test_create_postgres():
    pyversion = '3.8'
    docker = False
    flask = True

    create_postgres(pyversion, docker, flask)
    
    flask_postgres_files = ['flask_postgres_README.md', 'flask_postgres.py']
    assert root_path.joinpath('flask').is_dir()

    for file in flask_postgres_files:
        file_path = root_path.joinpath('flask', file)
        assert file_path.is_file()


def test_create_docker():
    # Test create_docker function
    pyversion = '3.8'

    create_docker(pyversion)
    
    docker_files = ['Dockerfile','.dockerignore']
    for file in docker_files:
        file_path = root_path.joinpath(file)
        assert file_path.is_file()


def test_create_fastapi():
    # Test create_fastapi function
    docker = False
    poetry = False

    fastapi_files = ['fastapi_app.py', 'fastapi_models.py', 'fastapi_database.py']
    create_fastapi(docker, poetry)

    assert root_path.joinpath('fastapi').is_dir()

    for file in fastapi_files:
        file_path = root_path.joinpath('fastapi', file)
        assert file_path.is_file()

