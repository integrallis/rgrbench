"""Tic Tac Toe Game - Integration Tests - Following STRICT TDD"""

from fastapi.testclient import TestClient
from tictactoe_game.main import app


def test_health_check_returns_200():
    """Test 1: Health check endpoint returns 200"""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_new_game():
    """Test 2: POST /api/games creates a new game"""
    client = TestClient(app)
    response = client.post("/api/games")
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["status"] == "in_progress"
    assert data["current_player"] == "X"
    assert data["board"] == ["", "", "", "", "", "", "", "", ""]


def test_make_move_in_game():
    """Test 3: POST /api/games/{game_id}/moves makes a move"""
    client = TestClient(app)
    # Create a game first
    game_response = client.post("/api/games")
    game_id = game_response.json()["id"]

    # Make a move
    move_data = {"position": 0}
    response = client.post(f"/api/games/{game_id}/moves", json=move_data)
    assert response.status_code == 200
    data = response.json()
    assert data["board"][0] == "X"
    assert data["current_player"] == "O"


def test_move_to_occupied_position_returns_400():
    """Test 4: Making a move to occupied position returns 400"""
    client = TestClient(app)
    # Create a game
    game_response = client.post("/api/games")
    game_id = game_response.json()["id"]

    # Make first move
    client.post(f"/api/games/{game_id}/moves", json={"position": 0})

    # Try to make move to same position
    response = client.post(f"/api/games/{game_id}/moves", json={"position": 0})
    assert response.status_code == 400
    assert "occupied" in response.json()["detail"].lower()


def test_get_game_by_id():
    """Test 5: GET /api/games/{id} returns game state"""
    client = TestClient(app)
    # Create a game
    game_response = client.post("/api/games")
    game_id = game_response.json()["id"]

    # Get the game
    response = client.get(f"/api/games/{game_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == game_id
    assert data["status"] == "in_progress"
    assert data["board"] == ["", "", "", "", "", "", "", "", ""]


def test_win_detection_horizontal():
    """Test 6: Game detects horizontal win"""
    client = TestClient(app)
    # Create a game
    game_response = client.post("/api/games")
    game_id = game_response.json()["id"]

    # Make moves to create horizontal win for X
    # X plays positions 0, 1, 2 (top row)
    # O plays positions 3, 4
    client.post(f"/api/games/{game_id}/moves", json={"position": 0})  # X
    client.post(f"/api/games/{game_id}/moves", json={"position": 3})  # O
    client.post(f"/api/games/{game_id}/moves", json={"position": 1})  # X
    client.post(f"/api/games/{game_id}/moves", json={"position": 4})  # O
    response = client.post(
        f"/api/games/{game_id}/moves", json={"position": 2}
    )  # X wins

    data = response.json()
    assert data["status"] == "won"
    assert data["winner"] == "X"


def test_draw_detection():
    """Test 7: Game detects draw when board is full with no winner"""
    client = TestClient(app)
    # Create a game
    game_response = client.post("/api/games")
    game_id = game_response.json()["id"]

    # Make moves to create a draw
    # Board will be:
    # X O X
    # X X O
    # O X O
    client.post(f"/api/games/{game_id}/moves", json={"position": 0})  # X
    client.post(f"/api/games/{game_id}/moves", json={"position": 1})  # O
    client.post(f"/api/games/{game_id}/moves", json={"position": 2})  # X
    client.post(f"/api/games/{game_id}/moves", json={"position": 5})  # O
    client.post(f"/api/games/{game_id}/moves", json={"position": 3})  # X
    client.post(f"/api/games/{game_id}/moves", json={"position": 6})  # O
    client.post(f"/api/games/{game_id}/moves", json={"position": 4})  # X
    client.post(f"/api/games/{game_id}/moves", json={"position": 8})  # O
    response = client.post(
        f"/api/games/{game_id}/moves", json={"position": 7}
    )  # X - board full

    data = response.json()
    assert data["status"] == "draw"
