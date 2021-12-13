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

def test_automl():
    # Test pyrepo easy pipeline
    runner = CliRunner()
   
    output_list = ['AutoML Implementation created']
    result = runner.invoke(main, ['easy', 'automl',  
                                        '-r','REPO_NAME',
                                        '-m', 'MAINTAINER',
                                        '-d', 'REPO_DESCRIPTION'])
    assert result.exit_code == 0
    
    for output in output_list:
        assert output in result.output


def test_fullml():
    # Test pyrepo easy pipeline
    runner = CliRunner()
   
    output_list = ['Full ML Implementation created']
    result = runner.invoke(main, ['easy', 'fullml',  
                                        '-r','REPO_NAME',
                                        '-m', 'MAINTAINER',
                                        '-d', 'REPO_DESCRIPTION'])
    assert result.exit_code == 0
    
    for output in output_list:
        assert output in result.output
    
    assert root_path.joinpath('ml','data').is_dir()


