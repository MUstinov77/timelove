from backend.app.app_factory import create_app
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)