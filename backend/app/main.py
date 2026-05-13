from fastapi import FastAPI

from backend.app.app_factory import create_app

app = create_app()


@app.get("/")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)