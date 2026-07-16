"""Minimal FastAPI app for Tic Tac Toe game"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Minimal storage
games = []
next_id = 1


class Move(BaseModel):
    position: int


@app.get("/health")
async def health_check():
    """Minimal health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/games", status_code=201)
async def create_game():
    """Create new tic tac toe game"""
    global next_id
    new_game = {
        "id": next_id,
        "status": "in_progress",
        "current_player": "X",
        "board": ["", "", "", "", "", "", "", "", ""],
    }
    games.append(new_game)
    next_id += 1
    return new_game


@app.get("/api/games/{game_id}")
async def get_game(game_id: int):
    """Get game by ID"""
    for game in games:
        if game["id"] == game_id:
            return game
    raise HTTPException(status_code=404, detail="Game not found")


def check_winner(board):
    """Check if there's a winner on the board"""
    # Winning combinations (rows, columns, diagonals)
    win_patterns = [
        [0, 1, 2],  # Top row
        [3, 4, 5],  # Middle row
        [6, 7, 8],  # Bottom row
        [0, 3, 6],  # Left column
        [1, 4, 7],  # Middle column
        [2, 5, 8],  # Right column
        [0, 4, 8],  # Diagonal
        [2, 4, 6],  # Anti-diagonal
    ]

    for pattern in win_patterns:
        if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != "":
            return board[pattern[0]]

    return None


@app.post("/api/games/{game_id}/moves")
async def make_move(game_id: int, move: Move):
    """Make a move in the game"""
    # Find the game
    game = None
    for g in games:
        if g["id"] == game_id:
            game = g
            break

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Check if position is already occupied
    if game["board"][move.position] != "":
        raise HTTPException(status_code=400, detail="Position is already occupied")

    # Make the move
    current_player = game["current_player"]
    game["board"][move.position] = current_player

    # Check for winner
    winner = check_winner(game["board"])
    if winner:
        game["status"] = "won"
        game["winner"] = winner
    # Check for draw (board full with no winner)
    elif all(cell != "" for cell in game["board"]):
        game["status"] = "draw"
    else:
        game["current_player"] = "O" if current_player == "X" else "X"

    return game
