import uvicorn
from app import create_app

app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, env_file=".env")
