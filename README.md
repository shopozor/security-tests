# Security tests

## Development setup

### Pre-commit hooks

Before committing anything, please run
```
pre-commit install
```
at the root of your clone of this repository.

### Virtual environment

You need to run the python tests in the virtual environment generated like this:
```
virtualenv venv
. venv/bin/activate
pip install -r tests/backend/requirements.txt
```

## Run the backend tests

See [the pipeline code](tests/Backend.groovy).
