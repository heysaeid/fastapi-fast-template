# FastAPI Fast Template
This library helps you not get involved in the complexities of FastAPI and its libraries and focus all your attention on the application.


## Features
- Proper structure and ready
- [Ruff](https://github.com/astral-sh/ruff) - An extremely fast Python linter and code formatter, written in Rust.
- [pre-commit](https://pre-commit.com/) - A framework for managing and maintaining multi-language pre-commit hooks.
- [fastapi-and-logging](https://github.com/heysaeid/fastapi-and-logging) - FastAPI-and-Logging simplifies log handling, allowing for effective organization, tracking, and analysis of logs in FastAPI applications, aiding in debugging and issue resolution.
- [fastapi-and-caching](https://github.com/heysaeid/fastapi-and-caching) - FastAPI and Caching is an extension for FastAPI that provides support for various caching mechanisms, allowing you to easily leverage caching within your FastAPI applications.
- [fastapi-and-babel](https://github.com/heysaeid/fastapi-and-babel.git) - FastAPIAndBabel allows you to easily use babel in your FastAPI projects and offers some features to improve and ease things.
- [APScheduler](https://apscheduler.readthedocs.io/en/3.x/) Advanced Python Scheduler (APScheduler) is a Python library that lets you schedule your Python code to be executed later, either just once or periodically.
- [FastStream](https://faststream.airt.ai/latest/) - the simplest way to work with a messaging queues



## Install
```
pip install git+https://github.com/heysaeid/fastapi-fast-template.git
```


# Usage
By executing the following command, you initiate the project configuration.

```shell
fast init
-- Enter the name of the application (default: Fast Template): FastTemplate
-- Enter the config module type (default: multiple): single or multiple
-- Enter the ORM (default: sqlalchemy): sqlalchemy or tortoise
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
        👉 FastAPI-And-Babel                  https://github.com/heysaeid/fastapi-and-babel
        👉 FastAPI-And-Logging                https://github.com/heysaeid/fastapi-and-logging
        👉 FastAPI-And-Caching                https://github.com/heysaeid/fastapi-and-caching
        👉 APScheduler                        https://fastapi.tiangolo.com
        👉 FastStream                         https://faststream.airt.ai
        And ...
        ___________________________________

```
