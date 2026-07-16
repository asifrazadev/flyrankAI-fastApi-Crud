# Task API — FlyRank Backend Internship · Week 2

A fully working **CRUD to-do list API** built with [FastAPI](https://fastapi.tiangolo.com/) and Python.  
Created as Week 2, Assignment A1 of the FlyRank Backend Internship.

---

## What this is

A REST API that lets any HTTP client **Create, Read, Update and Delete** tasks stored in memory.  
No database — data resets on restart (that's the lesson; Week 3 fixes it with a real DB).

**Swagger UI** is available at [`/docs`](http://localhost:8000/docs) — no extra setup needed.

---

## Install & run

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd flyrank-task-api

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn main:app --reload
```

Server runs at **http://localhost:8000**  
Interactive docs at **http://localhost:8000/docs**

---

## Endpoints

| Method | Path | Description | Success code |
|--------|------|-------------|--------------|
| `GET` | `/` | API info (name, version, endpoints) | 200 |
| `GET` | `/health` | Health check — `{"status":"ok"}` | 200 |
| `GET` | `/tasks` | List all tasks (supports `?done=` and `?search=` filters) | 200 |
| `GET` | `/tasks/{id}` | Get a single task by ID | 200 / 404 |
| `POST` | `/tasks` | Create a new task — body: `{"title": "..."}` | 201 / 400 |
| `PUT` | `/tasks/{id}` | Update `title` and/or `done` | 200 / 400 / 404 |
| `DELETE` | `/tasks/{id}` | Delete a task | 204 / 404 |
| `GET` | `/stats` | *(Extra)* Count total / done / open tasks | 200 |
| `POST` | `/reset` | *(Extra)* Restore the 3 seed tasks | 200 |

### Query parameters for `GET /tasks`

| Parameter | Type | Example | Effect |
|-----------|------|---------|--------|
| `done` | boolean | `?done=true` | Filter by completion status |
| `search` | string | `?search=milk` | Title contains keyword (case-insensitive) |

---

## Status codes used

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Successful GET or PUT |
| 201 | Created | Successful POST /tasks |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Missing or empty `title` |
| 404 | Not Found | No task with that ID |

---

## Sample `curl -i` output

```
$ curl -i http://localhost:8000/tasks/1
HTTP/1.1 200 OK
content-type: application/json
content-length: 56

{"id":1,"title":"Read the FastAPI docs","done":false}
```

```
$ curl -i http://localhost:8000/tasks/99
HTTP/1.1 404 Not Found
content-type: application/json

{"detail":"Task 99 not found"}
```

```
$ curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk"}'
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

```
$ curl -i -X DELETE http://localhost:8000/tasks/1
HTTP/1.1 204 No Content
```

---

## Swagger UI

All endpoints are documented and testable at **http://localhost:8000/docs**  
FastAPI generates the interactive docs automatically from the code — no extra config needed.

> _Screenshot: open `/docs` in your browser after starting the server to see all endpoints with "Try it out" buttons._

---

## The mortality experiment *(Extras)*

**Steps:**
1. `POST /tasks` to create a few new tasks
2. Stop the server (`Ctrl+C`)
3. Restart it (`uvicorn main:app --reload`)
4. `GET /tasks` — your new tasks are gone

**Why?** Tasks live in a Python list (`tasks = [...]`) — a variable in RAM.  
When the process dies, RAM is cleared. The 3 seed tasks come back because they're hardcoded in the source file.  
**This is why Week 3 introduces a real database** — a database writes to disk and survives restarts.

---

## Project structure

```
.
├── main.py           # All API logic (FastAPI app, endpoints, validation)
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## Tech stack

- **Python 3.10+**
- **FastAPI 0.115** — web framework + automatic OpenAPI/Swagger
- **Pydantic v2** — request body validation
- **Uvicorn** — ASGI server

---

*FlyRank Internship · Backend Track · Week 2 · Assignment A1*
