# TestDriven.io - Test-Driven Development with Django, Django REST Framework, and Docker

```bash
λ sqlite3 db.sqlite3
sqlite> .tables
sqlite> .schema TABLENAME
sqlite> .exit
```

```bash
λ docker-compose up -d --build
λ docker-compose exec movies python manage.py migrate --noinput
λ docker-compose exec movies-db psql --username=movies --dbname=movies_dev
```

```bash
psql (12.0)
Type "help" for help.

movies_dev=# \l
movies_dev=# \c movies_dev
movies_dev=# \dt
```

Inspect volume:

```bash
λ docker volume inspect django-tdd-docker_postgres_data
```

```bash
$ docker build -f ./app/Dockerfile -t hello_django:latest ./app
$ docker run -p 8001:8000 \
    -e "SECRET_KEY=please_change_me" -e "DEBUG=1" -e "DJANGO_ALLOWED_HOSTS=*" \
    hello_django python /usr/src/app/manage.py runserver 0.0.0.0:8000
```

## pytest

By default, pytest will autodiscover test files that start or end with `test` e.g., `test_*.py` or `*_test.py`. Test functions must begin with `test_`, and if you want to use classes they must also begin with `Test`.

Fixtures are reusable objects for tests.

They have associated scope, which informs how often the fixture is invoked:

* function - once per test function (default)
* class - once per test class
* module - once per test module
* session - once per test session (so, once actually)

They're perfect for setUp and tearDown resources used by tests.

```python
@pytest.fixture(scope="module")
def some_fixture():
    # set up code
    yield "value returned??"
    # tear down code
```

Follow Given-When-Then pattern:

Given: set the state of our application before test runs (setup code, fixtures, database state)
When: the behavior/logic being tested (code under test)
Then: expected changes after the previous behavior/logic (asserts)

## Django REST Framework

* composed mostly of 2 components
  * Serializers (convert Python (ex Django models) types to JSON (serialization) and vice versa (deserialization))
  * Views/ViewSets

### Serializers

By identifying certain fields as "read only", we can ensure that they will never be created or updated via the serializer.

## Tests

Running only tests, that contains `model` keyword, you can use:

```bash
λ docker-compose exec movies pytest -k models
```

DRF has three types of views

* Views (subclasses Django's View)
  * They can be function (implemented via the api_view decorator) or class (implemented via the APIView class) based
* ViewSets (provide a layer of abstraction above DRF views)
  * often used to combine CRUD logic into a single view
  * URL conventions will be consistent
* GenericViews
  * take the abstraction further by inferring the response format, allowed methods, and payload shape based on the serializer

To seed the database with some fixture/initial data:

```bash
λ docker-compose exec movies python manage.py flush
λ docker-compose exec movies python manage.py loaddata movies.json
```

```bash
# normal run
λ docker-compose exec movies pytest

# disable warnings
λ docker-compose exec movies pytest -p no:warnings

# run only the last failed tests
λ docker-compose exec movies pytest --lf

# run only the tests with names that match the string expression
λ docker-compose exec movies pytest -k "movie and not all_movies"

# stop the test session after the first failure
λ docker-compose exec movies pytest -x

# enter PDB after first failure then end the test session
λ docker-compose exec movies pytest -x --pdb

# stop the test run after two failures
λ docker-compose exec movies pytest --maxfail=2

# show local variables in tracebacks
λ docker-compose exec movies pytest -l

# list the 2 slowest tests
λ docker-compose exec movies pytest  --durations=2
```

## Heroku

```bash
# create application
λ heroku create
λ heroku container:login
# add PostgreSQL database
λ heroku addons:create heroku-postgresql:hobby-dev -a <heroku-app>
# Use heroku addons:docs heroku-postgresql to view documentation
λ docker build -f Dockerfile.prod -t registry.heroku.com/<heroku-app>/web .
λ docker push registry.heroku.com/<heroku-app>/web:latest
# Release the image
λ heroku container:release web
λ heroku config:set DJANGO_ALLOWED_HOSTS=<heroku-app>.herokuapp.com -a <heroku-app>
λ heroku run python manage.py migrate -a <heroku-app>
λ heroku run python manage.py loaddata movies.json -a <heroku-app>
λ http --json https://<heroku-app>.herokuapp.com/api/movies/
```

Build the production Docker image and tag it 

> Code coverage is the measure of how much code is executed during testing.

```bash
λ docker-compose up -d --build
λ docker-compose exec movies pytest -p no:warnings --cov=.
# or for HTML version:
λ docker-compose exec movies pytest -p no:warnings --cov=. --cov-report html
λ docker-compose exec movies black --check --exclude=migrations .
λ docker-compose exec movies /bin/sh -c "isort ./*/*.py --check-only"
λ docker-compose exec movies /bin/sh -c "isort ./*/*.py --diff"
λ docker-compose exec movies /bin/sh -c "isort ./*/*.py"
```

> just because you have 100% test coverage doesn’t mean you're testing the right things.
> 