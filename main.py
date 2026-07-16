"""
FlyRank Internship · Backend Track · Week 2 · Assignment A1
Task API — complete version with Swagger UI and extras.

Stages:
  0  hello server
  1  root + health
  2  GET /tasks, GET /tasks/{id} with 404
  3  POST /tasks with validation
  4  PUT /tasks/{id}, DELETE /tasks/{id}
  5  Swagger UI descriptions + extras (filter, search, /stats, /reset)

Run with:  uvicorn main:app --reload
Docs at:   http://localhost:8000/docs
"""

import copy
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, field_validator
from typing import Optional

app = FastAPI(
    title="Task API",
    version="1.0",
    description=(
        "A CRUD to-do list API built for the **FlyRank Backend Internship — Week 2**.\n\n"
        "Data lives in memory only — restarting the server resets the list. "
        "That's intentional: it's the reason Week 3 introduces a real database."
    ),
)

# ---------------------------------------------------------------------------
# In-memory 'database'
# ---------------------------------------------------------------------------
SEED_TASKS = [
    {"id": 1, "title": "Read the FastAPI docs",  "done": False},
    {"id": 2, "title": "Build the CRUD API",     "done": False},
    {"id": 3, "title": "Push to GitHub",         "done": False},
]

tasks: list[dict] = copy.deepcopy(SEED_TASKS)
next_id: int = 4


def _find_task(task_id: int) -> dict:
    """Return the task with the given id, or raise 404."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------

class TaskCreate(BaseModel):
    """Body for POST /tasks — title is required."""
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

@app.get(
    "/",
    tags=["Meta"],
    summary="API info",
    description="Returns the API name, version, and a list of available endpoint paths.",
)
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/stats", "/health", "/reset"],
    }


@app.get(
    "/health",
    tags=["Meta"],
    summary="Health check",
    description=(
        "Returns `{\"status\": \"ok\"}` when the server is running. "
        "Real companies use this endpoint so load balancers can verify the service is alive."
    ),
)
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Read — with extras: filter by done, search by title
# ---------------------------------------------------------------------------

@app.get(
    "/tasks",
    tags=["Tasks"],
    summary="List all tasks",
    description=(
        "Returns every task. Use `?done=true/false` to filter by status, "
        "or `?search=keyword` to filter by title (case-insensitive)."
    ),
)
def list_tasks(
    done: Optional[bool] = Query(
        default=None,
        description="Filter by completion — `true` = finished, `false` = open.",
    ),
    search: Optional[str] = Query(
        default=None,
        description="Return only tasks whose title contains this string (case-insensitive).",
    ),
):
    result = tasks
    if done is not None:
        result = [t for t in result if t["done"] == done]
    if search:
        result = [t for t in result if search.lower() in t["title"].lower()]
    return result


@app.get(
    "/tasks/{task_id}",
    tags=["Tasks"],
    summary="Get a single task",
    description="Returns the task with the given ID, or **404** if it does not exist.",
)
def get_task(task_id: int):
    return _find_task(task_id)


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------

@app.post(
    "/tasks",
    status_code=201,
    tags=["Tasks"],
    summary="Create a new task",
    description=(
        "Creates a task from `{\"title\": \"...\"}`. "
        "Returns **201** with the new task. "
        "Returns **400** if `title` is missing or empty — the server never trusts the client."
    ),
)
def create_task(body: TaskCreate):
    global next_id
    new_task = {"id": next_id, "title": body.title, "done": False}
    tasks.append(new_task)
    next_id += 1
    return new_task


# ---------------------------------------------------------------------------
# Update & Delete
# ---------------------------------------------------------------------------

@app.put(
    "/tasks/{task_id}",
    tags=["Tasks"],
    summary="Update a task",
    description=(
        "Updates `title` and/or `done`. At least one field required. "
        "Returns **200** with the updated task, **400** for empty body, **404** for unknown ID."
    ),
)
def update_task(task_id: int, body: TaskUpdate):
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


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    tags=["Tasks"],
    summary="Delete a task",
    description=(
        "Removes the task. Returns **204 No Content** on success "
        "(success, nothing to say). Returns **404** for unknown ID."
    ),
)
def delete_task(task_id: int):
    task = _find_task(task_id)
    tasks.remove(task)


# ---------------------------------------------------------------------------
# Extras
# ---------------------------------------------------------------------------

@app.get(
    "/stats",
    tags=["Extras"],
    summary="Task statistics",
    description="Returns a count of total, completed, and open tasks.",
)
def get_stats():
    done_count = sum(1 for t in tasks if t["done"])
    return {"total": len(tasks), "done": done_count, "open": len(tasks) - done_count}


@app.post(
    "/reset",
    tags=["Extras"],
    summary="Reset to seed data",
    description=(
        "Restores the original 3 example tasks and clears any added tasks. "
        "Useful for demos and the mortality experiment."
    ),
)
def reset_tasks():
    global tasks, next_id
    tasks = copy.deepcopy(SEED_TASKS)
    next_id = 4
    return {"message": "Tasks reset to seed data", "tasks": tasks}
