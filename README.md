# Python 3.11+ FastAPI layered architecture template

Taken from [munchie](https://github.com/PastaCarbonara/Backend/).

Original template from [teamhide](https://github.com/teamhide/fastapi-boilerplate).

Currently does not contain a WebSocket example. The Munchie repository does.

## To install the template

Make sure you are using the right python version (3.11+).

```cmd
python --version
```

Then:

```cmd
python -m virualenv venv

.\venv\Scripts\activate

python -m pip install -r .\requirements.txt
```

Now to run the project:

```cmd
python main.py
```

Head to [localhost:8000/api/latest/docs](http://localhost:8000/api/latest/docs) to test it out.

## Update database

To add a migration:

```cmd
alembic revision -m "REVISION NAME" --autogenerate
```

To commit said migration:

```cmd
alembic upgrade head
```

## Testing code

Running unittests

```cmd
pytest
```

- `--tb=no` no error stacktraces
- `--disable-warnings` no warnings
- `-s` enable printing

Checking test coverage

```cmd
coverage run -m pytest

coverage html
```

or

```cmd
pytest --cov=api --cov=app --cov=core --cov-report=html --cov-fail-under=85
```

Running the linter

```cmd
python linting.py app
```

`app` indicates the folder, try `api` and `core` too.
