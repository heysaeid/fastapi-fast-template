# FastAPI Fast Template
This library helps you not get involved in the complexities of FastAPI and its libraries and focus all your attention on the application.


## Features
- Proper structure and ready
- Using babel for internationalization and localization - [fastapi-and-babel](https://github.com/heysaeid/fastapi-and-babel.git)
- Powerful logging tools using [fastapi-and-logging](https://github.com/heysaeid/fastapi-and-logging) - (supports logging incoming, outgoing, and error events.)
- Support for different backends for caching [fastapi-and-caching](https://github.com/heysaeid/fastapi-and-caching)
- Using [Ruff](https://github.com/astral-sh/ruff) as a linter and formatter.
- Using Git [pre-commit](https://pre-commit.com/).


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
