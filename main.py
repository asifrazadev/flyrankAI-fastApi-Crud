"""
FlyRank Internship · Backend Track · Week 2 · Assignment A1
Task API

Stage 2: In-memory task list + read endpoints (GET /tasks, GET /tasks/{id}).
Run with: uvicorn main:app --reload
"""

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A CRUD to-do list API built for the FlyRank Backend Internship — Week 2.",
)

# ---------------------------------------------------------------------------
# In-memory 'database' — data lives here while the server is running.
# Restarting the server resets the list (Week 3 fixes this with a real DB).
# ---------------------------------------------------------------------------
tasks: list[dict] = [
    {"id": 1, "title": "Read the FastAPI docs",  "done": False},
    {"id": 2, "title": "Build the CRUD API",     "done": False},
    {"id": 3, "title": "Push to GitHub",         "done": False},
]
next_id: int = 4


def _find_task(task_id: int) -> dict:
    """Return the task with the given id, or raise 404."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# ---------------------------------------------------------------------------
# Meta endpoints
# ---------------------------------------------------------------------------

@app.get("/", tags=["Meta"], summary="API info")
def root():
    """Returns the API name, version and available endpoints."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", tags=["Meta"], summary="Health check")
def health():
    """Returns ok when the server is alive. Used by monitoring tools."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Stage 2 — Read
# ---------------------------------------------------------------------------

@app.get("/tasks", tags=["Tasks"], summary="List all tasks")
def list_tasks():
    """Returns every task in the in-memory list."""
    return tasks


@app.get("/tasks/{task_id}", tags=["Tasks"], summary="Get a single task")
def get_task(task_id: int):
    """
    Returns the task with the given ID.
    Returns **404** if no task has that ID — never return an empty 200.
    """
    return _find_task(task_id)
