"""
FlyRank Internship · Backend Track · Week 2 · Assignment A1
Task API

Stage 4: Full CRUD — PUT /tasks/{id} and DELETE /tasks/{id}.
Run with: uvicorn main:app --reload
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import Optional

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
# Request models
# ---------------------------------------------------------------------------

class TaskCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("title must not be empty")
        return v.strip()


class TaskUpdate(BaseModel):
    """Body for PUT /tasks/{id} — both fields optional, at least one required."""
    title: Optional[str] = None
    done: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("title must not be empty")
        return v.strip() if v else v


# ---------------------------------------------------------------------------
# Meta
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
# Create
# ---------------------------------------------------------------------------

@app.post("/tasks", status_code=201, tags=["Tasks"], summary="Create a new task")
def create_task(body: TaskCreate):
    """
    Creates a task — body: `{"title": "..."}`.
    Returns **201** with the new task, or **400** if title is missing/empty.
    """
    global next_id
    new_task = {"id": next_id, "title": body.title, "done": False}
    tasks.append(new_task)
    next_id += 1
    return new_task


# ---------------------------------------------------------------------------
# Stage 4 — Update & Delete
# ---------------------------------------------------------------------------

@app.put("/tasks/{task_id}", tags=["Tasks"], summary="Update a task")
def update_task(task_id: int, body: TaskUpdate):
    """
    Updates `title` and/or `done` on the specified task.

    - At least one field must be provided — otherwise **400**.
    - Unknown ID → **404**.
    - Returns the updated task on success (**200**).
    """
    if body.title is None and body.done is None:
        raise HTTPException(
            status_code=400,
            detail="Request body must include at least one of: title, done",
        )
    task = _find_task(task_id)
    if body.title is not None:
        task["title"] = body.title
    if body.done is not None:
        task["done"] = body.done
    return task


@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"], summary="Delete a task")
def delete_task(task_id: int):
    """
    Removes the task with the given ID.

    - Returns **204 No Content** on success (nothing to say — it's gone).
    - Unknown ID → **404**.
    """
    task = _find_task(task_id)
    tasks.remove(task)
