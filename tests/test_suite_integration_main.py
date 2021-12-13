import pytest
import pathlib
from configparser import ConfigParser
from click.testing import CliRunner
import pdb
import shutil

from src.flask_app.setup_flask import flask
from src.dash.setup_dash import dash
from src.cicd.githubactions import github_actions, lambda_workflow
from src.cicd.circleci import cci
from src.virtual_environment.virtual_environment import poetry, virtualenv
from src.postgres.postgres import postgres
from src.docker.docker import docker
from src.templater import main, easy, easy_setup
from src.fastapi.setup_fastapi import fastapi

# pytest sets cwd as the repository root
root_path = pathlib.Path().cwd()
BASE_PATH = pathlib.Path.cwd()

# ============================================================= #
#                     TEST CLICK COMMANDS                       #
# ============================================================= #
# These integration tests mostly cover two things,
# 1. successful completion with exit code 0
# 2. expected output on cli
# Unit tests will test behavior more specifically and can be found in test_suite_unit.py

def test_easy_setup():
    runner = CliRunner()
    
    output_list = ['Setting config...',
                    'Settings saved as config.toml',
                    'installing', 
                    'requirements',
                    'Activate Virtual Environment'] 
    with runner.isolated_filesystem():
        result = runner.invoke(main,
                            ['easy-setup'],
                            input="\n".join(['Repo_Name', 'Repo_Description']))
    
    assert result.exit_code == 0
    for output in output_list:
        assert output in result.output
    assert "Activate Virtual Environment with .\\env\\Scripts\\Activate.ps1 or if using command prompt use .\\env\\Scripts\\activate.bat. Use deactivate to exit virtual environment" not in result.output


def test_inspect_pass():
    # Test the inspect cli function to failure
    runner = CliRunner()
    result = runner.invoke(main, ['inspect'])
    assert result.exit_code == 0
    assert 'Repo_Name' in result.output
    assert 'Repo_Description' in result.output


def test_inspect_fail():
    # Test the inspect cli function to failure
    # Remove config if exists
    config_path = root_path.joinpath('config.toml')
    if config_path.exists():
        config_path.unlink()
    runner = CliRunner()
    result = runner.invoke(main, ['inspect'])
    assert result.exit_code == 1
    assert 'No configuration has been set...' in result.output


def test_lambda_workflow():
    # Test pyrepo easy lambda-workflow command
    runner = CliRunner()
    output_list = ['Setting up Lambda workflow...',
                    'Lambda Setup Complete, see configuration in .github/workflows/lambda.yml']
    with runner.isolated_filesystem():
        result = runner.invoke(main, ['easy', 'lambda-workflow'])
        config_path = root_path.joinpath('.github', 'workflows', 'lambda.yml')
        assert result.exit_code == 0
        assert config_path.is_file()
        for output in output_list:
            assert output in result.output


def test_easy_flask_docker():
    # Test pyrepo easy flask command, docker option
    runner = CliRunner()
   
    output_list = ['Github actions created',
                    'Flask Application setup is complete. See configuration in flask/app.py',
                    'Dockerfile has been integrated. See configuration in ./Dockerfile'] 
    

    result = runner.invoke(main,
                        ['easy', 'flask', '--docker'],
                        input="\n".join(['Repo_Name', 'Repo_Description','Maintainer', 'y']))

    assert result.exit_code == 0
    for output in output_list:
        assert output in result.output


def test_easy_flask_nodocker():
    # Test pyrepo easy flask command, no docker option
    runner = CliRunner()
   
    output_list = ['Github actions created',
                    'Flask Application setup is complete. See configuration in flask/app.py']

    result = runner.invoke(main,
                        ['easy', 'flask'],
                        input="\n".join(['Repo_Name', 'Repo_Description', 'Maintainer', 'N', 'y']))

    assert result.exit_code == 0
    for output in output_list:
        assert output in result.output
    assert 'Dockerfile has been integrated. See configuration in ./Dockerfile' not in result.output


def test_easy_dash_basic():
    # Test pyrepo easy dash command, basic option
    runner = CliRunner()
   
    output_list = ['Importing basic Dash files...',
                    'Dockerfile has been integrated. See configuration in ./Dockerfile',
                    'Dash files have been setup. Run Python dash-basic/dash_basic_template.py to launch server']

    result = runner.invoke(main,
                        ['easy', 'dash', '--basic', '--docker'],
                        input='\n'.join(['Repo_Name', 'Repo_Description', 'Maintainer', 'y']))
    
    assert result.exit_code == 0
    for output in output_list:
        assert output in result.output


def test_easy_dash_gis():
    # Test pyrepo easy dash command, basic option
    runner = CliRunner()
   
    output_list = ['Importing gis Dash files...',
                    'Dash files have been setup. Run Python dash-gis/dash_gis_template.py to launch server']
        
       
    result = runner.invoke(main,
                        ['easy', 'dash', '--gis', '--docker'],
                        input='\n'.join(['Repo_Name', 'Repo_Description', 'Maintainer', 'y']))
    assert result.exit_code == 0
    for output in output_list:
        assert output in result.output
    
    assert 'Poetry Setup Complete, see configuration in pyproject.toml' not in result.output
    assert 'Importing basic Dash files...' not in result.output


def test_easy_github_actions():
    # Test pyrepo easy github-actions command
    runner = CliRunner()
   
    output_list = ['Setting up Github Actions workflow...',
                    'Github Actions Setup Complete, see configuration in .github/workflows/workflow_*.yml'] 
    with runner.isolated_filesystem():
        result = runner.invoke(main, ['easy', 'github-actions'])
    
    assert result.exit_code == 0
    for output in output_list:
        assert output in result.output


def test_cci():
    # Test pyrepo easy cci command
    runner = CliRunner()
   
    output_list = ['Setting up CircleCI workflow...',
                    'CircleCI Setup Complete, see configuration in .circleci/config.yml'] 
    
    with runner.isolated_filesystem():
        result = runner.invoke(main, ['easy', 'cci'])
    
    assert result.exit_code == 0
    for output in output_list:
        assert output in result.output


def test_poetry():
    # Test pyrepo easy poetry command
    runner = CliRunner()
   
    output_list = ['Setting up Poetry Virtual Environment Configuration...',
                    'Poetry Setup Complete, see configuration in pyproject.toml']
    with runner.isolated_filesystem():
        result = runner.invoke(main,
                            ['easy', 'poetry',
                            '-r','REPO_NAME',
                            '-m', 'MAINTAINER',
                            '-d', 'REPO_DESCRIPTION'])

    assert result.exit_code == 0
    for output in output_list:
        assert output in result.output


def test_virtualenv():
    # Test pyrepo easy virtualenv command (successful run and expected cli output)
    runner = CliRunner()
   
    output_list = ['Setting up Virtualenv Virtual Environment Configuration...',
                    'Setup of virtual environment complete, environment located in ./env folder']

    with runner.isolated_filesystem():
        path_in = BASE_PATH.joinpath('templates', 'flask_requirements.txt')
        path_out = BASE_PATH.joinpath('requirements.txt')
        shutil.copyfile(path_in, path_out)
        result = runner.invoke(main, ['easy', 'virtualenv'])
    assert result.exit_code == 0
    for output in output_list:
        assert output in result.output


def test_postgres():
    # Test pyrepo easy postgres command
    runner = CliRunner()
   
    output_list = ['Flask Application setup is complete. See configuration in flask/app.py',
                    'Creating Postgres files...',
                    'Postgres integration files have been setup. Please see flask_postgres_README.md for instructions on how to set up Postgres credentials and DB tables via CLI.']

    result = runner.invoke(main,
                        ['easy',
                        'postgres',
                        '--flask',
                        '--docker',
                        '-r','REPO_NAME',
                        '-m', 'MAINTAINER',
                        '-d', 'REPO_DESCRIPTION'])
    
    assert result.exit_code == 0
    for output in output_list:
        assert output in result.output
    

def test_docker():
    # Test pyrepo easy docker command
    runner = CliRunner()
   
    output_list = ['Dockerfile has been integrated. See configuration in ./Dockerfile. Reference .dockerignore for files to exclude from the build image.'] 
    with runner.isolated_filesystem():
        result = runner.invoke(main, ['easy', 'docker'])
    
    assert result.exit_code == 0
    
    for output in output_list:
        
        assert output in result.output


def test_fastapi():
    # Test pyrepo easy fastapi command
    runner = CliRunner()
    
    output_list = ['Github actions created',
                    'Navigate to and run fastapi/fastapi_app.py to start your app',
                    'Dockerfile has been integrated. See configuration in ./Dockerfile. Reference .dockerignore for files to exclude from the build image.']
     
    with runner.isolated_filesystem():
        result = runner.invoke(main,
                            ['easy', 'fastapi', '--docker'],
                            input='\n'.join(['Repo_Name', 'Repo_Description', 'Maintainer', 'y']))
    assert result.exit_code == 0
    for output in output_list:
        assert output in result.output


def test_config_setup_one():
    # Test pyrepo config, first combination of settings
    runner = CliRunner()
   
    output_list = ['Setting config...',
                    'Settings saved as config.toml',
                    'Creating github actions workflow...',
                    'You have decided to use Docker',
                    'Create flask application...',
                    'Adding postgres database...',
                    'Repository Setup Complete',
                    'Feel free to delete templates folder'
                    ]
    with runner.isolated_filesystem():
        result = runner.invoke(main,
                            ['config',
                            '--docker',
                            '--ecr',
                            '--flask',
                            '--postgres',
                            '-r','REPO_NAME',
                            '-m', 'MAINTAINER',
                            '-d', 'REPO_DESCRIPTION'])
        
        assert result.exit_code == 0
        for output in output_list:
            assert output in result.output
        assert 'Importing basic Dash files...' not in result.output


