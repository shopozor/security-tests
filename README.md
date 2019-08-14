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
pip install -r backend/requirements.txt
```

## Run the backend tests

In order to run the tests, you need to do the following:
```
. venv/bin/activate
cd backend
pytest --domain http://shopozor-backend.hidora.com --graphql-endpoint graphql/ -ra --junitxml=../reports/backend.xml
```