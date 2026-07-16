"""
FlyRank Internship · Backend Track · Week 2 · Assignment A1
Task API

Stage 3: Create endpoint — POST /tasks with input validation.
Run with: uvicorn main:app --reload
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A CRUD to-do list API built for the FlyRank Backend Internship — Week 2.",
)

# ---------------------------------------------------------------------------
# In-memory 'database'
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
# Stage 3 — Request model (Pydantic validates the body automatically)
# ---------------------------------------------------------------------------

class TaskCreate(BaseModel):
    """Body for POST /tasks."""
    title: str

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("title must not be empty")
        return v.strip()


# ---------------------------------------------------------------------------
# Meta endpoints
# ---------------------------------------------------------------------------

@app.get("/", tags=["Meta"], summary="API info")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", tags=["Meta"], summary="Health check")
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------

@app.get("/tasks", tags=["Tasks"], summary="List all tasks")
def list_tasks():
    """Returns every task in the in-memory list."""
    return tasks


@app.get("/tasks/{task_id}", tags=["Tasks"], summary="Get a single task")
def get_task(task_id: int):
    """Returns one task by ID, or 404 if not found."""
    return _find_task(task_id)


# ---------------------------------------------------------------------------
# Stage 3 — Create
# ---------------------------------------------------------------------------

@app.post(
    "/tasks",
    status_code=201,
    tags=["Tasks"],
    summary="Create a new task",
)
def create_task(body: TaskCreate):
    """
    Creates a task from the JSON body `{"title": "..."}`.

    - Returns **201 Created** with the new task.
    - Returns **400 Bad Request** if `title` is missing or empty.
    The server never trusts the client — title is always validated.
    """
    global next_id
    new_task = {"id": next_id, "title": body.title, "done": False}
    tasks.append(new_task)
    next_id += 1
    return new_task
