Contributor Guidelines
==============================

If you would like to help extend the functionality of the python-repo-template, or suggest a fix, please adhere to the following guidelines.
This is meant to be a general guide of expectations to help facilitate your contribution to the python-repo-template.

- [Contributor Guidelines](#contributor-guidelines)
  - [General Recipe](#general-recipe)
  - [Issues](#issues)
  - [git](#git)
  - [static typing](#static-typing)
  - [unit testing](#unit-testing)

General Recipe
---
The general flow of contribution is as follows
1. Verify that your new feature is not already implemented in the repo by checking the src/ folder for list of current features:                                                         ![image](https://user-images.githubusercontent.com/66369718/116105743-9a04df00-a67f-11eb-868f-7bcc772fdbc9.png)

2. Open a new issue on the python-repo-template, describing your desired fix/feature. Tag repository contributors to give visibility.
3. If the feature is given the go ahead, clone the master branch to your development environment from github.com
4. Ensure your python environment is 3.7+. If it is not, please update your development environment to the latest python release.
5. Create a new branch from master
6. Push the branch to github for visibility
7. If you are adding sub-feature to an existing feature, add the logic inside of .py file within the feature's folder. For example:                                                     ![image](https://user-images.githubusercontent.com/66369718/116108466-ebae6900-a681-11eb-84c8-5ab8469677f0.png)

   1. If a sub-feature is being add to the flask feature then add feature logic inside of setup_flask.py unless it makes more sense to create a separate .py file
   
   2. Connect logic in feature folder to the src/templater.py file
   
   3. Add all files that will be included in the new feature/sub-feature into the /templates folder
          ![image](https://user-images.githubusercontent.com/66369718/116109366-b22a2d80-a682-11eb-9a8e-e9a9daa98fe9.png)

8. Continue to commit your changes to the branch
   1. Use PEP8 as a style guide. Ideally, you are using a linter in the IDE, and ideally that IDE is [Visual Studio Code](https://code.visualstudio.com/).
   2. Commits should use descriptive language so someone else can know what you did.
   3. Rigorously test your new feature in a local environment
   4. Write unit tests to ensure the reliabilty of the new feature and to communicate the feature's intent.
   5. All functions and classes should contain docstrings in the [numpy format](https://numpydoc.readthedocs.io/en/latest/format.html) as code documentation
9. When you have a Proof of Concept/80% solution, open a Pull Request
   1. CI/CD workflows will run to check the code, including any unit tests you have written.
   2. A form will be created when the PR is created and should be filled out in its entirety. The checkboxes can be checked after the PR is submitted, on github.com. 
   3. The results of the automated workflows and the information in the form will be used to assess the submission
10. Link the Pull Request to the issue opened in step 2, if applicable

Issues
---
When a bug is located or a new feature is needed, open a new issue for python-repo-template on [github.com](https://github.com/gh-ai-solu/python-repo-template). Describe the problem at a high level, and any suggested solutions. Issues with suggested solutions will get higher priority than those without.

git
---
Github Flow is the required model for contributing to python-repo-template. See the git section in the [README](README.md) for more information.

static typing
---
All functions in the repository code must contain static type hints. This repository includes automatic Github Workflow checks that run mypy against all files in the templates/ and src/ directories on a PR event. Adding functions and classes that do not contain type hints will fail the automatic checks when a PR is created to merge the code into master. See the static typing section in the [README](README.md) or [mypy documentation](https://mypy.readthedocs.io/en/stable/index.html) for more information about static typing, mypy, and its usage in this template.

unit testing
---
Unit tests are expected to be created for every new function/class added to python-repo-template. Unit tests help to ensure the quality of code under constantly changing conditions. Furthermore, they help to communicate the intent of code modules, as a developer can refer to the unit tests and see how the function is expected to behave. See the Unit Testing section of [README](README.md) for more information. Also see [pytest](https://docs.pytest.org/en/stable/) to learn more about the testing framework used in python on this project.

