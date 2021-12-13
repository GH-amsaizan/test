Python Repo Template
==============================
![](https://github.com/gh-ai-solu/python-repo-template/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/gh-ai-solu/python-repo-template/branch/master/graph/badge.svg?token=GELBJWMRSU)](https://codecov.io/gh/gh-ai-solu/python-repo-template)

Table of Contents
- [Python Repo Template](#python-repo-template)
  - [Start Here](#start-here)
    - [Easy Control](#easy-control)
    - [Finer Control](#finer-control)
    - [Get **help** using the CLI](#get-help-using-the-cli)
    - [Inspect current settings in config.toml](#inspect-current-settings-in-configtoml)
    - [After Finishing Configuration](#after-finishing-configuration)
  - [Utilities Included](#utilities-included)
  - [Contributing to python-repo-template](#contributing-to-python-repo-template)
  - [Template Folder Structure](#template-folder-structure)
  - [CI/CD Integration](#cicd-integration)
    - [Github Actions](#github-actions)
      - [YAML Syntax](#yaml-syntax)
      - [Optional Last Step for Github Actions](#optional-last-step-for-github-actions)
    - [CircleCI](#circleci)
  - [Unit Testing](#unit-testing)
    - [Setup](#setup)
    - [Writing Unit Test Tutorial](#writing-unit-test-tutorial)
    - [Folder Structure for Integration Tests](#folder-structure-for-integration-tests)
  - [Static type checking with mypy](#static-type-checking-with-mypy)
    - [Static typing](#static-typing)
    - [Mypy notes](#mypy-notes)
    - [Mypy  usage](#mypy--usage)
    - [Suggested flags](#suggested-flags)
    - [Writing functions with static type hints](#writing-functions-with-static-type-hints)
    - [Static typing with pandas example](#static-typing-with-pandas-example)
  - [Machine Learning](#machine-learning)
    - [AutoML](#automl)
    - [Full ML](#full-ml)
    - [Helpful Links](#helpful-links)
  - [Github Permissions](#github-permissions)
  - [Code Coverage](#code-coverage)
  - [Generate Documentation](#generate-documentation)
  - [Virtual Environments](#virtual-environments)
    - [Which VE managers can we use?](#which-ve-managers-can-we-use)
    - [Setup](#setup-1)
    - [Caveats for use](#caveats-for-use)
  - [Code Profiling](#code-profiling)
  - [git Branching Models](#git-branching-models)

Start Here
---
1. Generate a new repository with the template on Github by clicking  [here](https://github.com/gh-ai-solu/python-repo-template/generate) or by navigating  [here](https://github.com/gh-ai-solu/python-repo-template) and clicking the "Use Template" button
2. Clone the repository you just created to your development environment
3. In a CLI, `cd` into the repository root directory
4. Install the `pyrepo` package:
    
    `pip install -e .`
5. The `pyrepo` command line program is now installed. Learn more by running `pyrepo --help`

### Easy Control
- Run the following for easy setup

    `pyrepo easy-setup`


>OR


### Finer Control
-   For more in depth control of setup, the preferred way is to use

    `pyrepo config`

    To see all the configuration options use

    `pyrepo config --help`

-   Another option for finer control is to run individual pyrepo commands for service/use case setup using the settings in config.toml if no arguments provided, or by using CLI flags, which can be found by running `pyrepo --help` and `pyrepo <command> --help`. This allows the user to mix and match configurations as needed, allowing maximum flexibility for project setup.

    `pyrepo easy flask`

    `pyrepo easy fastapi`
    
	`pyrepo easy github`

    `pyrepo easy docker`
	
	`pyrepo easy circleci`
	
	`pyrepo easy poetry`
	
	`pyrepo easy virtualenv`
	
	`pyrepo easy dash`
	
### Get **help** using the CLI
-   `pyrepo inspect`

### Inspect current settings in config.toml
-   `pyrepo inspect`


### After Finishing Configuration
- Feel free to delete the following files and folders once setup is complete
  -   **templates** folder - the template files it contains are not needed post setup.
  -   **setup.py** - pyrepo has already been installed in your  environment
  -   **pyrepo.egg-info** folder - this will cause pyrepo not to work on command line, so if you would like to keep the pyrepo tool installed, then keep this folder but add it to .gitignore
- To uninstall `pyrepo`
  - `pip uninstall pyrepo`
  - Delete the **pyrepo.egg-info** folder in the repository root

Utilities Included
---
python-repo-template will install several useful utilities during the setup process, but that don't require any configuration right off the bat. These utilities include:
- **pdoc3** : python package to generate autodocs. See section [Generate Docs](#generate-documentation) for usage.
- **pyinstrument** : code profiling package, see section [Code Profiling](#code-profiling) for more information
- **[mypy](https://mypy.readthedocs.io/en/stable/)** : Static type checking for python. See [Static Type Checking with mypy](#static-type-checking-with-mypy) for detailed instructions

Contributing to python-repo-template
---
If you would like to contribute to the python-repo-template codebase, see [Contributing.md](CONTRIBUTING.md) for more details.

Template Folder Structure
---

    ├── .circleci	       <- CircleCI configuration
	│
	├── .github	           <- Github Actions configuration
    │
    ├── docs               <- Source code documentation, PR template
    │
	├── src                <- Source code for use in this project
    │
	├── templates          <- Jinja templates for config files
	│
	├── Dockerfile         <- Manifest file to build a basic python based docker image/container
	│
    ├── CONTRIBUTING.md    <- Developer Guidelines for extending the repo template and fixing bugs 
    │
	├── README.md          <- The top-level README for developers using this template. Pattern your project README.md after this one
    │
	├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g. generated with `pip freeze > requirements.txt`                     
    │
	├── setup.py           <- setup file for installing pyrepo cli/package


CI/CD Integration
---
### Github Actions
Github Actions is a Github built in **CI/CD** suite of tools that enables automation and integration. It is suitable for **general projects** and is the current preferred tool for cloud integration. There are many actions that Github can perform that may be useful for your project. These workflows include but aren't limited to the following use cases...

    A. Unit Testing
    B. Integration Testing
    C. Linting
    D. Code Coverage
    E. Build and Push Docker Images to a registry
    F. Secrets Detection

The *workflow_dev_\*.yml* and *workflow_master_\*.yml* files created during setup already contain many but not all of these utilities. They are located in the .github/workflows/ directory if Github Actions was selected and can be edited to tailor the pipeline to the project's needs.

#### YAML Syntax
For a good introduction to writing yaml syntax in context of Github Actions, see [here](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)

#### Optional Last Step for Github Actions
**Add** badges to **README.md**: The badges give a snapshot of the health of the repository code base. You will quickly be able to tell if your Github Actions workflow has run successfully on a specific branch, and if your code coverage is adequate. The badges will resemble this image below. Simply copy the badge markup from this README.md file into your repo README.md file, replacing the repository name and branch information as needed. If the badge is a code coverage badge, it will require additional setup to work depending on the code coverage service you use.

![](https://www.michalbialecki.com/wp-content/uploads/2020/01/ga-badges.png)

### CircleCI
If your repo requires **CircleCI** integration, complete the following steps
- Use the `pyrepo config` or `pyrepo setup-circleci` commands to setup a workflow. Remember that the repository will need to be enabled to integrate with CircleCI.

- On CircleCI, under Projects, find your repo and click `Set Up Project` then click `Use Existing Config`. CircleCI will now run on the prescribed Github events as defined in your config.yml file, which can be found in the .circleci directory.

If desired, **status badges** can be added for CircleCI builds.
 
- See documentation [here](https://circleci.com/docs/2.0/status-badges/)

## Unit Testing
### Setup
If you have not written any tests for your code, if it will eventually be deployed, then unit tests must be written to ensure code quality. See [here](https://docs.pytest.org/en/stable/) for details about writing unit tests using pytest (preferred method which works right out of the box with Github Actions). Eighty percent code coverage is an achievable goal for any project (see [Code Coverage](#code-coverage) section for more detail)

**Add tests to your project** >> write test functions in a file named similar to test_*.py. This can be located in a tests/ folder or in src/. If you are unfamiliar with writing unit tests, see [Writing Unit Test Tutorial](#writing-unit-test-tutorial) for an introduction and [here](https://docs.pytest.org/en/stable/) for the pytest documentation.

**Run pytest manually, outside of a pipeline** >> In a CLI, `cd` into the repository root or the directory that contains test_funcs.py and run `pytest`, which will generate the test results in standard output.

### Writing Unit Test Tutorial
Let's say we have a function that computes the factorial of number, located in a program called **main.py**, in the src directory.

```python
def factorial(num):
    '''
    Calculate factorial recursively
	
    Parameters
    ----------
    num : integer
        Iterable object
        
    Returns
    -------
    float
        calculated factorial
    '''
	
    if num == 1:
        return 1
    return num*factorial(num-1)
```
We want to test that the function executes correctly, so we will write a unit test. A unit test is meant to test one specific piece of code functionality, hence the name "unit". Any python program whose name is prefixed with "test_\*" will be detected by [pytest](https://docs.pytest.org/en/stable/index.html) as containing testing functions and any functions prefixed with "test_\*" in those files will be executed as unit tests when `pytest` is run. Here is the structure of our unit test for the factorial() function.

```python
import math	
def test_factorial():
    '''Test factorial function'''
    value = 20
    f = func.factorial(value)
    assert f == math.factorial(value)
```
Tests are evaluated using plain `assert` statements within a test function. Multiple assert statements can be placed in one function, however it is best practice to create a unique function for each assertion most of the time, one assertion per condition you want to test.


Running command `pytest` in the repository root, or the src directory (manually or in a Github Action/ CircleCI workflow), will detect test functions and execute them. The CLI output of a pytest run will look like this...

**Note:** `pytest` is not installed by default when you use the `pyrepo` setup tool. If you will be running unit tests locally, please add it to your dependencies.

![pytest](/docs/pytest.png)



### Folder Structure for Integration Tests
pytest is lenient on folder structure for unit tests but gets more opionated when integration tests are run. The following folder structure is suggested and has been proven on actual projects.
```
root
 ┣ app
 ┃ ┣ assets
 ┃ ┃ ┗ style.css
 ┃ ┣ src
 ┃ ┃ ┣ module1.py
 ┃ ┃ ┣ module2.py
 ┃ ┃ ┣ CustomClass.py
 ┃ ┃ ┗ __init__.py
 ┃ ┣ tests
 ┃ ┃ ┣ conftest.py
 ┃ ┃ ┣ test_dash.py
 ┃ ┃ ┗ __init__.py
 ┃ ┣ .dockerignore
 ┃ ┣ app.py
 ┃ ┣ docker-compose.yml
 ┃ ┣ Dockerfile
 ┃ ┣ requirements.txt
 ┃ ┗ __init__.py
 ┣ docs
 ┃ ┗ documentation.md
 ┣ .gitignore
 ┗ README.md
  
 ```
Your particular use case may be different. The main point is to allow for and implement absolute imports of modules in the code so that pytest will run the integration tests smoothly.

An example absolute import in app.py would be... 
```python 
from src import module1
from src.module2 import some_function
```
## Static type checking with mypy
### Static typing
Statically typed programming languages require you to state the type of your variables before using them. Python, however, is a dynamically typed language. This provides more flexibility for writing code, but can lead to issues at runtime. We encourage static typing in order to catch these issues earlier in the development process. For more information on static and dynamic typing, see [Dynamic typing vs static typing](https://docs.oracle.com/cd/E57471_01/bigData.100/extensions_bdd/src/cext_transform_typing.html).

### Mypy notes
To allow for static type checking in your repository, we have included `mypy` as a utility. `mypy` offers type checking with various capabilities to suit project needs. Primarily, we recommend all functions have static type annotations to minimize errors in code functionality. All functions included in source code and templates are already statically typed, but `mypy` offers a way to check and ensure static typing for additional code written. For a detailed explanation of `mypy` and usage instructions, see [the mypy documentation](https://mypy.readthedocs.io/en/stable/index.html).

### Mypy  usage
`mypy` can be [used from a CLI](https://mypy.readthedocs.io/en/stable/command_line.html#command-line), [set up in a configuration file](https://mypy.readthedocs.io/en/stable/config_file.html), or [run in an application](https://mypy.readthedocs.io/en/stable/extending_mypy.html). This repo contains a `mypy` config file, `mypy.ini`, that allows a user to quickly type check all code except files in the tests folder. To run `mypy` on the repo via the config file, navigate to the root directory in a CLI and run `mypy .`. The CLI also provides more flexibility to check individual files or use different flags. Additionally, the Github actions/CircleCi workflows in this template have been integrated with `mypy` to automatically type check after certain actions.

### Suggested flags
The `mypy` config file and CI/CD workflows use the following flags when type checking with `mypy`:
- `ignore-missing-imports`: This flag tells mypy not to type check imported libraries that aren't currently compatible with `mypy` type checking
- `disallow-untyped-defs`: This flag tells `mypy` to throw an error if any functions are without proper static typing annotations
- `deny-any-explicit`: This flag prohibits the use of the `Any` type, a catch-all that restricts the effectiveness of `mypy` by not forcing developers to include a specifc type in annotations

There may be times when `mypy` gives an error that can be ignored, but it is recommended that your code pass the check from the config file. For more information about `mypy` flags, see [here](https://mypy.readthedocs.io/en/stable/command_line.html).

### Writing functions with static type hints
Adding static type hints to a Python function is a fairly simple process. Each function must have type hints indicated for all arguments and a specify a return type. Function calls then must pass the proper variable types, and the function's return statement must match the specific return type. Some types (bool, int, str, etc.) will be automatically recognized, but others (List, Dict, Tuple, etc.) must be brought in via import statements. The function written below shows an example of a function with correct formatting and usage of static typing hints.

```python
from typing import List

def hints_example(name: str, address: str) -> List:
    '''Make list from a name and address'''
    return [name, address]
```
The function requires two strings to be passed in, representing a name and address. It then returns these two strings as two elements in a list, as indicated by the return type.

### Static typing with pandas example
In addition to the standard Python types, `mypy` is also able to recognize select additional types from commonly used libraries. When possible, importing the relevant types will allow `mypy` to recognize them and pass the check without errors. The following shows an example of a statically-typed function using `pandas` types.

```python
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series

def test_pandas_static(test_df: DataFrame) -> Series:
    '''Test static typing with pandas'''
    test_series = df.iloc[:,1]
    return test_series
```
Using the import statements and type annotations on the function, mypy is able to recognize that `test_df` should be a pandas DataFrame and that the function should return a pandas Series. `test_df` is sliced into `test_series`, and mypy recognizes the return value as a pandas Series. This function passes the `mypy` type checking using the three flags mentioned in the previous section.

## Machine Learning
The CLI tool pyrepo has two different levels of machine learning capability built in, AutoML and Full ML Pipeline.

### AutoML
The AutoML implementation uses mljar-supervised under the hood. To execute the AutoML code on a toy problem, run `python automl.py` after activating the virtual environment. Each time the command is run, it will auto generate a new output folder with all analyses results.

### Full ML
The Full ML implementation is built on top of DVC and MLFLow. The typical entry point for running your ml pipeline will be `dvc repro`. Several things need to happen before the pipeline will be able to produce any meaningful results.
1. The data must be populated in the correct folders under the ml/data directory. These files can be placed directly in their respective directories or can be managed with the `dvc remote` command if they are stored remotely from your dev environment. The stage files (.py files) already contain some pathlib helper code to import the data into the python runtime.
2. All .py files in ml/ need to be coded according to their task within the pipeline. Very minimal code is included in these files because no assumptions can be made as to the nature of the data cleaning or modeling process.
3. If you wish to implement MLFLow for tracking ML experiments and models or creating a model registry, additional steps are necessary. See below for the link.

### Helpful Links
[AutoML Implementation](https://github.com/mljar/mljar-supervised)

[DVC](https://dvc.org/)

[MlFlow](https://github.com/mlflow/mlflow)

## Github Permissions
It is important to set controls on your repository to avoid headaches down the road. It is best practice to set permissions for individual users only up to what is required for the job, and no more.

As a start, **Set permissions** on github.com within your repo that prevent a merge to master without review, and that require there to be one review that is initiated by a PR using the template. See this [link](https://docs.github.com/en/github/administering-a-repository/enabling-required-reviews-for-pull-requests) for instructions. The Branch name pattern can be `master` or `default`. Also check `Dismiss stale pull request approvals...` option.

## Code Coverage 
Code coverage is how much of your code base executes when the unit testing is performed. It is a measure of confidence that the code will do the task it was designed for. Once unit testing has been incorporated into the repo, the repository can be integrated with codecov.com

**Set** code coverage secrets in repo. To avoid proliferating codecov accounts, contact Carlos Brown (cabrown@guidehouse.com) or Charles Landau (clandau@guidehouse.com) to set github secrets and integrate codecov for your repo.

[link](https://www.codecov.io)

## Generate Documentation
Proper documentation of a project is important. Documentation can be **auto-generated** using **pdoc3**. 

Run `pdoc --force --html ../path/to/file.py`. Pdoc will generate documentation based on docstrings for functions and classes defined in file.py.

Documentation should be stored in the docs folder and can be designated using the `--output-dir` flag in `pdoc`

For information on how to write docstrings for functions and classes in the numpy style, see [here](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html). To automate docstring creation, search for `njpwerner.autodocstring` under Extensions in [VS Code](https://code.visualstudio.com/)

## Virtual Environments

### Which VE managers can we use?
This template supports the use of two different environment managers out of the box...

1. [**Poetry**](https://python-poetry.org/)
2. [**venv**](https://docs.python.org/3/library/venv.html)

### Setup
Preferred: `pyrepo config` or `pyrepo easy`

Alternate: `pyrepo setup-poetry` or `pyrepo setup-virtualenv` to install the virtual environment of your choice in the repository. Note that his will not interfere with dockerization of the application. Typically, a manifest file (requirements.txt or pyproject.toml) is necessary to recreate the python environment in the docker container, so there is **synergy** between using a virtual environment for local dev alongside a docker image.

>Python virtual environments in a docker container can help with [Multi-Stage Builds](https://docs.docker.com/develop/develop-images/multistage-build/) to cut down on docker image size and "attack surface" if the app will be deployed on the web.

### Caveats for use
`pyrepo` will setup the environment differently based on your choice of manager.

* Poetry: `pyrepo` creates the pyproject.toml file
* venv: `pyrepo` creates the env folder, and if requirements.txt is detected in the repo root, it will install these requirements if the system is Windows. Otherwise, it will simply create a basic environment that will require manual install of requirements. After the environment is set or changed, the requirements.txt file should be refreshed with the following command in the repo root:
```pip freeze > requirements.txt```

>It is the responsibility of the developer to update the environment as packages change. python-repo-template simply performs the initial setup and install, it does not perform dependency management throughout the lifecycle of the project.


## Code Profiling
Sometimes you need to find out why your code is so inefficient, identify bottlenecks, and find areas of improvement. The recommended tool to use is `pyinstrument`. Run `pyinstrument -r html -o <outfile_save_location> your_script.py` to generate the profiling report in html for your code run.


## git Branching Models

There are multiple approaches to how code contribution should be organized in git version control. For introductions to the different models, see [here](https://medium.com/@patrickporto/4-branching-workflows-for-git-30d0aaee7bf).

Unless there is a prescribed branching model for your project, the [Github Flow](http://scottchacon.com/2011/08/31/github-flow.html) is a good basic model to follow 



--------
