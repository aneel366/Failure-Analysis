from fastapi import FastAPI

from app.routes.failure_routes import router as failure_router

app = FastAPI(title="Failure Analysis API", version="1.0.0")
app.include_router(failure_router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "failure-analysis"}
