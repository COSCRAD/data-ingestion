# COSCRAD Data Ingestion

## Setup

Make sure you are using Python 3.10.16.

If using VS Code, install Microsoft's Python, Pylance, and Python Debugger extensions.

Create a virtual environment:
If using VS Code, create a virtual environment by using `CTRL + SHIFT + P` and running the command`Python: Create Environment...` (python.createEnvironment). Ensure that you have configured VS Code to format on save.

If using the terminal, create a virtual environment as follows:

> > > python -m venv .venv

Install PIP dependencies:

> > > pip install -U pip
> > > pip install -r requirements.txt

## Development

Activate the virtual environment:

> > > source .venv/bin/activate

Run the tests using the `testing`plugin in VS Code. Alternatively, you can use the command line as follows:

> > > python3 -m pytest
