# Python 3.11+ FastAPI layered architecture template

Taken from [munchie](https://github.com/PastaCarbonara/Backend/).

Original template from [teamhide](https://github.com/teamhide/fastapi-boilerplate).

Currently does not contain a WebSocket example. The Munchie repository does.

## To install the template

Make sure you are using the right python version.

`python --version`

Then:

`python -m virualenv venv`

`.\venv\Scripts\activate`

`python -m pip install -r .\requirements.txt`

Now to run the project:

`python main.py`

Head to [localhost:8000/api/latest/docs](http://localhost:8000/api/latest/docs) to test it out.

## Update database

To add a migration:

`alembic revision -m "REVISION NAME" --autogenerate`

To commit said migration:

`alembic upgrade head`

## Testing code

Running unittests

`pytest`

- `--tb=no` no error stacktraces
- `--disable-warnings` no warnings
- `-s` enable printing

Checking test coverage

`coverage run -m pytest`

`coverage html`

or

`pytest --cov=api --cov=app --cov=core --cov-report=html --cov-fail-under=70`
