"""Todo App - Integration Tests - Following STRICT TDD"""

import main
from fastapi.testclient import TestClient
from main import app


def test_health_check_returns_200():
    """Test 1: Health check endpoint returns 200"""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_todos_returns_empty_list():
    """Test 2: GET /api/todos returns empty list initially"""
    client = TestClient(app)
    response = client.get("/api/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_todo():
    """Test 3: POST /api/todos creates a new todo"""
    client = TestClient(app)
    todo_data = {"title": "Buy groceries", "completed": False}
    response = client.post("/api/todos", json=todo_data)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Buy groceries"
    assert data["completed"] is False


def test_get_todo_by_id():
    """Test 4: GET /api/todos/{id} returns specific todo"""
    client = TestClient(app)
    # First create a todo
    todo_data = {"title": "Test todo", "completed": False}
    create_response = client.post("/api/todos", json=todo_data)
    todo_id = create_response.json()["id"]

    # Now get it by ID
    response = client.get(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test todo"
    assert data["completed"] is False


def test_update_todo():
    """Test 5: PUT /api/todos/{id} updates a todo"""
    client = TestClient(app)
    # First create a todo
    todo_data = {"title": "Original title", "completed": False}
    create_response = client.post("/api/todos", json=todo_data)
    todo_id = create_response.json()["id"]

    # Update it
    update_data = {"title": "Updated title", "completed": True}
    response = client.put(f"/api/todos/{todo_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Updated title"
    assert data["completed"] is True


def test_delete_todo():
    """Test 6: DELETE /api/todos/{id} removes a todo"""
    client = TestClient(app)
    # First create a todo
    todo_data = {"title": "To be deleted", "completed": False}
    create_response = client.post("/api/todos", json=todo_data)
    todo_id = create_response.json()["id"]

    # Delete it
    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 204

    # Verify it's gone (should return 404 now)
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_todo_returns_404():
    """Test 7: GET /api/todos/{id} returns 404 for non-existent todo"""
    client = TestClient(app)
    response = client.get("/api/todos/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_nonexistent_todo_returns_404():
    """Test 8: PUT /api/todos/{id} returns 404 for non-existent todo"""
    client = TestClient(app)
    update_data = {"title": "Updated", "completed": True}
    response = client.put("/api/todos/9999", json=update_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_create_todo_with_due_date():
    """Test 9: POST /api/todos creates a todo with due date"""
    client = TestClient(app)
    todo_data = {"title": "Pay bills", "completed": False, "due_date": "2025-01-15"}
    response = client.post("/api/todos", json=todo_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Pay bills"
    assert data["completed"] is False
    assert data["due_date"] == "2025-01-15"


def test_create_todo_with_priority():
    """Test 10: POST /api/todos creates a todo with priority"""
    client = TestClient(app)
    todo_data = {"title": "Fix critical bug", "completed": False, "priority": "high"}
    response = client.post("/api/todos", json=todo_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Fix critical bug"
    assert data["priority"] == "high"


def test_filter_todos_by_status():
    """Test 11: GET /api/todos?completed=true filters by completion status"""
    # Reset global state
    main.todos = []
    main.next_id = 1

    client = TestClient(app)

    # Create some todos with different completion status
    client.post("/api/todos", json={"title": "Completed task", "completed": True})
    client.post("/api/todos", json={"title": "Incomplete task", "completed": False})
    client.post("/api/todos", json={"title": "Another completed", "completed": True})

    # Filter completed todos
    response = client.get("/api/todos?completed=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(todo["completed"] is True for todo in data)
