[![FastAPI and Pytest CI](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml/badge.svg)](https://github.com/mbrav/signup_api/actions/workflows/fastapi.yml)

## FastAPI tasks_api (based on [signup_api](https://github.com/mbrav/signup_api))

An 100% asynchronous Fast API service for tasks.

### Client-server application.

#### Server

Responsible for receiving and completing tasks. Tasks are executed strictly in turn and one at a time, sequentially. Processing client requests and executing tasks are done asynchronously.

Provides the following interface:

1. Gets the task type and data and adds the task to the execution queue. Returns the task ID.
2. Returns the status of the task by ID (for example: queued, in progress, completed)
    - Tasks can be edited and postponed;
    - Tasks can be deleted;
    - Tasks can be aborted
3. By identifier returns the result of the task execution (provide that the result can be accessed several times).

Storage of tasks (identifiers, data, and results) are done in a PostgreSQL database via [asyncpg](https://github.com/MagicStack/asyncpg)

The list of tasks (type) is predefined, to simulate the duration of the task, add the specified delay during its execution:

##### 1. Reverse a string example

**(example -> elpmaxe)**
Delay by 10 seconds since creation.

To execute the following code:

```python
async def reverse(text: str) -> str:
    return text[::-1]
```

A POST request to `/api/tasks` such as this must be made:

```json
{
	"name": "reverse",
	"qwargs": {
		"text": "hello"
	},
	"delay_seconds": 10
}
```

### Stack

The project uses [FastAPI](https://fastapi.tiangolo.com/) as a base framework with the following stack:

-   Integration with [SQLAlchemy's](https://www.sqlalchemy.org/) new ORM statement paradigm to be implemented in [v2.0](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html);
-   Asynchronous PostgreSQL database via [asyncpg](https://github.com/MagicStack/asyncpg), one of the fastest and high performant Database Client Libraries for python/asyncio;
-   A token authorization system using the [argon2 password hashing algorithm](https://github.com/P-H-C/phc-winner-argon2), the password-hashing function that won the [Password Hashing Competition (PHC)](https://www.password-hashing.net/);
-   Asynchronous task scheduling using [apscheduler](https://github.com/agronholm/apscheduler)

### Run FastAPI backend in Docker

Copy .env file:

```bash
cp backend/.env.example backend/.env
```

With docker-compose installed, do:

```bash
docker-compose up
```

Go to [localhost/docs](http://0.0.0.0/docs) for SwaggerUI

Token auth for superuser permissions:

-   **User**: `admin`
-   **Password**: `password`
