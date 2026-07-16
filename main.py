"""
FlyRank Internship · Backend Track · Week 2 · Assignment A1
Task API

Stage 1: Root and health endpoints.
Run with: uvicorn main:app --reload
"""

from fastapi import FastAPI

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A CRUD to-do list API built for the FlyRank Backend Internship — Week 2.",
)


@app.get("/", tags=["Meta"], summary="API info")
def root():
    """Returns the API name, version and available endpoints."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get("/health", tags=["Meta"], summary="Health check")
def health():
    """Returns ok when the server is alive. Used by monitoring tools."""
    return {"status": "ok"}
