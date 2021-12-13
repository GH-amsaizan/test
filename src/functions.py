from jinja2 import Environment, FileSystemLoader
import sys
from pathlib import Path


SYS_PY = f"{sys.version_info.major}.{sys.version_info.minor}"
BASE_PATH = Path.cwd()


def create_template_env(BASE_PATH: Path = BASE_PATH) -> Environment:
    # Load Jinja environment and grab templates
    template_path = BASE_PATH.joinpath("templates")
    file_loader = FileSystemLoader(str(template_path))
    env = Environment(loader=file_loader)
    return env


def squash_requirement_files(x: str) -> str:
    # Get jinja environment
    env = create_template_env()
    # requirements_template is grabbing the .txt file within the templates folder
    requirements_template = env.get_template(x)
    # root_requirements_template is grabbing the requirements.txt at the root directory
    root_requirements_template = Environment(loader=FileSystemLoader(str(BASE_PATH))).get_template('requirements.txt')
    # output combines the two .txt files into one
    output = requirements_template.render() + '\n' + root_requirements_template.render()
    
    return output


