"""Minimal FastAPI app to pass tests"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Minimal storage
todos = []
next_id = 1


class TodoCreate(BaseModel):
    title: str
    completed: bool = False
    due_date: str | None = None
    priority: str | None = None


class TodoUpdate(BaseModel):
    title: str
    completed: bool


@app.get("/health")
async def health_check():
    """Minimal health check endpoint"""
    return {"status": "healthy"}


@app.get("/api/todos")
async def get_todos(completed: bool | None = None):
    """Get todos with optional filtering by status"""
    if completed is not None:
        return [todo for todo in todos if todo["completed"] == completed]
    return todos


@app.post("/api/todos", status_code=201)
async def create_todo(todo: TodoCreate):
    """Minimal create todo endpoint"""
    global next_id
    new_todo = {"id": next_id, "title": todo.title, "completed": todo.completed}
    if todo.due_date:
        new_todo["due_date"] = todo.due_date
    if todo.priority:
        new_todo["priority"] = todo.priority
    todos.append(new_todo)
    next_id += 1
    return new_todo


@app.get("/api/todos/{todo_id}")
async def get_todo(todo_id: int):
    """Get todo by ID - with 404 handling"""
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.put("/api/todos/{todo_id}")
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """Update todo by ID - with 404 handling"""
    for todo in todos:
        if todo["id"] == todo_id:
            todo["title"] = todo_update.title
            todo["completed"] = todo_update.completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/api/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    """Delete todo by ID - minimal implementation"""
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    return None
