[![FastAPI and Pytest CI](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml/badge.svg)](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml)

## FastAPI tasks_api

An asynchronous Fast API service for tasks.

### Client-server application.

#### Server

Responsible for receiving and completing tasks. Tasks are executed strictly in turn and one at a time, sequentially. Processing client requests and executing tasks should be done in parallel.

Provides the following interface:

1. Gets the task type and data and adds the task to the execution queue. Returns the task ID.
2. Returns the status of the task by ID (for example: queued, in progress, completed)
3. By identifier returns the result of the task execution (provide that the result can be accessed several times).

Storage of tasks (identifiers, data, and results) between server runs is not required.

The list of tasks (type) is predefined, to simulate the duration of the task, add the specified delay during its execution:

1. Reverse the line. (example -> remirp). Delay 2 sec.
2. Perform a pairwise permutation of even and odd characters in the string (example -> rpworld, cat -> oct). Delay 5 sec.
3. Repeat a character in a string according to its position (example -> prriimmmeeeeerrrrr). Delay 7 sec.

#### Customer

Serves to execute requests to the server (it is recommended to use command line parameters).
Should be able to:

1. Pass the data and task type to the server, display the identifier.
2. Request and display the task status by ID.
3. Request and display the result of the task execution by ID.
4. Ability to run in (batch) mode, when the client, having received the task type and data:
    - submits the task for execution and displays the identifier
    - waiting for the task to be completed (while waiting, you can display the current status)
    - requests and displays the result of the task execution.
    - can interrupt the wait by ctrl+c

### Stack

The project uses [FastAPI](https://fastapi.tiangolo.com/) as a base framework with the following stack:

-   Integration with [SQLAlchemy's](https://www.sqlalchemy.org/) new ORM statement paradigm to be implemented in [v2.0](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html);
-   Asynchronous PostgreSQL databse via [asyncpg](https://github.com/MagicStack/asyncpg), one of the fastest and high performant Database Client Libraries for python/asyncio;
-   A token authorization system using the [argon2 password hashing algorithm](https://github.com/P-H-C/phc-winner-argon2), the password-hashing function that won the [Password Hashing Competition (PHC)](https://www.password-hashing.net/);
-   Asynchronous pytests using [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) and [httpx](https://www.python-httpx.org/) libraries instead of the synchronous requests library;

### Run FastAPI backend in Docker

Copy .env file:

```bash
$ cp backend/.env.example backend/.env
```

With docker-compose installed, do:

```bash
docker-compose up
```

Go to [localhost/docs](http://0.0.0.0/docs) for SwaggerUI

Token auth for superuser permissions:

-   User: `admin`
-   Password: `password`
