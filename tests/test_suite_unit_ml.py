import pytest
import pathlib
import sys


from src.ml.setup_ml import create_automl, create_fullml

# pytest sets cwd as the repository root
root_path = pathlib.Path().cwd()

SYS_PY = f"{sys.version_info.major}.{sys.version_info.minor}"


def test_create_automl():
    # Test create_automl behavior
    create_automl()
    assert root_path.joinpath('ml', 'automl.py').is_file()


def test_create_fullml():
    # Test create_automl behavior
    create_fullml()
    assert root_path.joinpath('ml', 'dvc.yaml').is_file()
    


