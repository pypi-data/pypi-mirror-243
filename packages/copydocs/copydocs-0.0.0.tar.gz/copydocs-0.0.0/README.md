# copydocs [![Package version](https://img.shields.io/pypi/v/copydocs?label=PyPI)](https://pypi.org/project/copydocs) [![Supported Python versions](https://img.shields.io/pypi/pyversions/copydocs.svg?logo=python&label=Python)](https://pypi.org/project/copydocs)
[![Tests](https://github.com/bswck/copydocs/actions/workflows/test.yml/badge.svg)](https://github.com/bswck/copydocs/actions/workflows/test.yml)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/bswck/copydocs.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/bswck/copydocs)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg?label=Code%20style)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/bswck/copydocs.svg?label=License)](https://github.com/bswck/copydocs/blob/HEAD/LICENSE)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

DRY: Reuse your docstrings.


# Installation
If you want to…


## …use this tool in your project 💻
You might simply install it with pip:

    pip install copydocs

If you use [Poetry](https://python-poetry.org/), then run:

    poetry add copydocs

## …contribute to [copydocs](https://github.com/bswck/copydocs) 🚀

Happy to accept contributions!

> [!Note]
> If you use Windows, it is highly recommended to complete the installation in the way presented below through [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).

First, [install Poetry](https://python-poetry.org/docs/#installation).<br/>
Poetry is an amazing tool for managing dependencies & virtual environments, building packages and publishing them.

    pipx install poetry

<sub>If you encounter any problems, refer to [the official documentation](https://python-poetry.org/docs/#installation) for the most up-to-date installation instructions.</sub>

Be sure to have Python 3.8 installed—if you use [pyenv](https://github.com/pyenv/pyenv#readme), simply run:

    pyenv install 3.8

Then, run:

    git clone https://github.com/bswck/copydocs path/to/copydocs
    cd path/to/copydocs
    poetry env use $(cat .python-version)
    poetry install
    poetry shell
    pre-commit install --hook-type pre-commit --hook-type pre-push


# Legal info
© Copyright by Bartosz Sławecki ([@bswck](https://github.com/bswck)).<br />This software is licensed under the [MIT License](https://github.com/bswck/copydocs/blob/main/LICENSE).

