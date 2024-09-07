# FastAPI Fast Template
[![Package version](https://img.shields.io/pypi/v/fastapi-fast-template?color=%2334D058&label=pypi%20package)](https://pypi.org/project/fastapi-fast-template/)
[![Downloads](https://img.shields.io/pypi/dm/fastapi-fast-template)](https://pypi.org/project/fastapi-fast-template/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/fastapi-fast-template.svg?color=%2334D058)](https://pypi.org/project/fastapi-fast-template/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/heysaeid/fastapi-fast-template/blob/master/LICENSE)

This library helps you not get involved in the complexities of FastAPI and its libraries and focus all your attention on the application.


## Features
- Proper structure and ready
- [Ruff](https://github.com/astral-sh/ruff) - An extremely fast Python linter and code formatter, written in Rust.
- [pre-commit](https://pre-commit.com/) - A framework for managing and maintaining multi-language pre-commit hooks.
- [SQLAlchemy](https://sqlalchemy.org/) - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL
- [Tortoise ORM](https://tortoise.github.io/) - Tortoise ORM is an easy-to-use asyncio ORM (Object Relational Mapper) inspired by Django.
- [SQLModel ORM](https://sqlmodel.tiangolo.com/) - SQLModel, SQL databases in Python, designed for simplicity, compatibility, and robustness.
- [Beanie ODM](https://beanie-odm.dev/) - Beanie - is an asynchronous Python object-document mapper (ODM) for MongoDB.
- [fastapi-and-logging](https://github.com/heysaeid/fastapi-and-logging) - FastAPI-and-Logging simplifies log handling, allowing for effective organization, tracking, and analysis of logs in FastAPI applications, aiding in debugging and issue resolution.

- [fastapi-and-caching](https://github.com/heysaeid/fastapi-and-caching) - FastAPI and Caching is an extension for FastAPI that provides support for various caching mechanisms, allowing you to easily leverage caching within your FastAPI applications.
- [fastapi-and-babel](https://github.com/heysaeid/fastapi-and-babel.git) - FastAPIAndBabel allows you to easily use babel in your FastAPI projects and offers some features to improve and ease things.
- [APScheduler](https://apscheduler.readthedocs.io/en/3.x/) Advanced Python Scheduler (APScheduler) is a Python library that lets you schedule your Python code to be executed later, either just once or periodically.
- [FastStream](https://faststream.airt.ai/latest/) - the simplest way to work with a messaging queues
- [Authx](https://github.com/yezz123/AuthX) - Ready-to-use and customizable Authentications and Oauth2 management for FastAPI ⚡
- [FastAPI Cloud Auth(<b style="color:green">Coming Soon...</b>)](https://github.com/tokusumi/fastapi-cloudauth)
- [FastAPI Admin(<b style="color:green">Coming Soon...</b>)](https://github.com/fastapi-admin/fastapi-admin)
- [FastAPI MVC(<b style="color:green">Coming Soon...</b>)](https://github.com/fastapi-mvc/fastapi-mvc)
- [Fastapi-mail(<b style="color:green">Coming Soon...</b>)](https://github.com/sabuhish/fastapi-mail)


## Install
```
pip install fastapi-fast-template
```


# Usage
By executing the following command, you initiate the project configuration.

```shell
fast init
-- Enter the name of the application (default: Fast Template): FastTemplate
-- Enter the config module type (default: multiple): single or multiple
-- Enter the ORM/ODM (default: sqlalchemy): sqlalchemy, tortoise, sqlmodel or beanie
Initializing has been done successfully.
```
🥳🥳, your project has been created!


```
.
├── logs/
├── src/
│   ├── models/
│   ├── repositories/
│   │   ├── base.py
│   ├── routers/
│   │   ├── __init__.py
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   │   ├── lifespan.py
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
├── tests/
├── LICENSE
├── .env
├── .env.sample
├── .fast_template.ini
├── .gitignore
├── .pre-commit-config.yaml
└── ruff.toml
```
Now, you can run it as follows.
```shell
python src/main.py
INFO:     Will watch for changes in these directories: ['.']
INFO:     Loading environment from '.env'
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [44167] using StatReload
INFO:     Started server process [44175]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Extensions
### Babel
You can add Babel to your project as follows.
```
fast extension --name babel
Please select the default language (default: en): fa
...
...
...
compiling catalog translations/fa/LC_MESSAGES/messages.po to translations/fa/LC_MESSAGES/messages.mo

```
For more information, [click here](https://github.com/heysaeid/fastapi-and-babel).

<hr>

### APScheduler
You can add APScheduler to your project as follows.
```
fast extension --name scheduler
```
To use it, you can check the "tasks" directory and the "\_\_init__.py" module.
```python
from tasks import scheduler

async def fast_template_scheduler():
    print("FastAPI Fast Template")

scheduler.add_job(
    func = fast_template_scheduler,
    trigger = CronTrigger(minute = "*/30", timezone = "Asia/Tehran")
)
```
By running the project, the scheduler is executed.

For more information, [click here](https://apscheduler.readthedocs.io/en/3.x/).
<hr>

### FastAPI-And-Caching
You can add caching to your project as follows.
```
fast extension --name caching
```

To use it, you can check the "utils" directory and the "caching.py" module.
```python
from utils.caching import cache

@app.get("/")
@cache.cached(key="root", expire=30, prefix="router")
def root():
    return "FastAPI Fast Template"
```

For more information, [click here](https://github.com/heysaeid/fastapi-and-caching).

<hr>

### FastAPI-And-Logging
You can add logging to your project as follows.
```
fast extension --name logging
Please select the log type (default: incoming): (choose from incoming, apicall, exception)
```
You can now check out the app.py module and apply your changes to it.

For more information, [click here](https://github.com/heysaeid/fastapi-and-logging).

<hr>

### FastStream
You can add broker to your project as follows.
```
fast extension --name stream
Please select the broker (default: redis): (choose from redis, aiokafka, confluent, rabbit, nats)
```
You can run it with the following command
‍‍‍‍‍
```shell
faststream run src.stream:app
```

For more information, [click here](https://github.com/airtai/faststream).


## Documents
You can have direct access to the documentation of each library used by using the following command.
```shell
fast doc


        Quick access to the documents of the tools used in this template.
        ___________________________________

        👉 FastAPI                            https://fastapi.tiangolo.com
        👉 SQLAlchemy                         https://www.sqlalchemy.org
        👉 Tortoise ORM                       https://tortoise.github.io
        👉 SQLModel ORM                       https://sqlmodel.tiangolo.com
        👉 Beanie ODM                         https://beanie-odm.dev
        👉 FastAPI-And-Babel                  https://github.com/heysaeid/fastapi-and-babel
        👉 FastAPI-And-Logging                https://github.com/heysaeid/fastapi-and-logging
        👉 FastAPI-And-Caching                https://github.com/heysaeid/fastapi-and-caching
        👉 APScheduler                        https://fastapi.tiangolo.com
        👉 FastStream                         https://faststream.airt.ai
        👉 AuthX                              https://github.com/yezz123/authx
        And ...
        ___________________________________

```
