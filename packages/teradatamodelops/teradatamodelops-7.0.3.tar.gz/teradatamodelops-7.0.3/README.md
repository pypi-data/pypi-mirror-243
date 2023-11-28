# Teradata ModelOps Python Client
[![Build Status](https://azuredevops.td.teradata.com/NewCollection/ModelOps/_apis/build/status/ModelOpsPythonSDK?repoName=ModelOps%2FModelOpsPythonSDK&branchName=master)](https://azuredevops.td.teradata.com/NewCollection/ModelOps/_build/latest?definitionId=7&repoName=ModelOps%2FModelOpsPythonSDK&branchName=master)
![PyPI](https://img.shields.io/pypi/v/teradatamodelops)

Python client for Teradata ModelOps. It is composed of both a client API implementation to access the ModelOps backend APIs and a command line interface (cli) tool which can be used for many common tasks. 


## Requirements

Python 3.7+


## Usage

See the pypi [guide](./docs/pypi.md) for some usage notes. 


## Installation

To install the latest release, just do

```bash
pip install teradatamodelops
```

To build from source, it is advisable to create a Python venv or a Conda environment 

Python venv:
```bash
python -m venv tmo_python_env
source tmo_python_env/bin/activate
```

Install library from local folder using pip:

```bash
pip install . --use-feature=in-tree-build
```

Install library from package file

```bash
# first create the package
python setup.py clean --all
python setup.py sdist bdist_wheel

# install using pip
pip install dist/*.whl
```

## Testing

```bash
pip install -r dev_requirements.txt
python -m pytest
```

## Building and releasing 

Assuming PyPi credentials are configured in  `~/.pypirc`
```bash
python -m pip install --user --upgrade setuptools wheel twine

rm -rf dist/ 

python setup.py sdist bdist_wheel

twine upload dist/*
```
