"""
Tests for the Maze Walker kata (tddbuddy.com/katas/maze-walker).
String-art mazes: '#'/'*' walls, ' '/'.' corridors, one 'S' start, one 'E'
exit. The walker returns the shortest orthogonal path as (x, y) coordinates.
"""

import pytest


def test_straight_corridor_path() -> None:
    """Test 1: A straight corridor is walked cell by cell from S to E"""
    from maze_walker import walk_maze

    maze = "\n".join(
        [
            "#####",
            "#S E#",
            "#####",
        ]
    )

    assert walk_maze(maze) == [(1, 1), (2, 1), (3, 1)]


def test_start_next_to_exit_gives_a_two_cell_path() -> None:
    """Test 2: Adjacent S and E produce a path of exactly two coordinates"""
    from maze_walker import walk_maze

    maze = "\n".join(
        [
            "####",
            "#SE#",
            "####",
        ]
    )

    assert walk_maze(maze) == [(1, 1), (2, 1)]


def test_dots_are_corridors_too() -> None:
    """Test 3: '.' cells are walkable like spaces"""
    from maze_walker import walk_maze

    maze = "\n".join(
        [
            "#####",
            "#S.E#",
            "#####",
        ]
    )

    assert walk_maze(maze) == [(1, 1), (2, 1), (3, 1)]


def test_l_shaped_path_turns_a_corner() -> None:
    """Test 4: The walker follows a corridor that bends"""
    from maze_walker import walk_maze

    maze = "\n".join(
        [
            "####",
            "#S##",
            "# ##",
            "# E#",
            "####",
        ]
    )

    assert walk_maze(maze) == [(1, 1), (1, 2), (1, 3), (2, 3)]


def test_walker_takes_the_shortest_of_two_routes() -> None:
    """Test 5: With a 5-step and a 9-step route, the 5-step route is returned"""
    from maze_walker import walk_maze

    maze = "\n".join(
        [
            "#######",
            "#S   E#",
            "# ### #",
            "#     #",
            "#######",
        ]
    )

    path = walk_maze(maze)

    assert len(path) == 5
    assert path == [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]


def test_walker_navigates_around_a_dividing_wall() -> None:
    """Test 6: The single route around a dividing wall is followed exactly"""
    from maze_walker import walk_maze

    maze = "\n".join(
        [
            "#######",
            "#S    #",
            "##### #",
            "#E    #",
            "#######",
        ]
    )

    assert walk_maze(maze) == [
        (1, 1),
        (2, 1),
        (3, 1),
        (4, 1),
        (5, 1),
        (5, 2),
        (5, 3),
        (4, 3),
        (3, 3),
        (2, 3),
        (1, 3),
    ]


def test_every_step_is_orthogonal_and_path_spans_start_to_exit() -> None:
    """Test 7: Consecutive coordinates differ by one square, never diagonally"""
    from maze_walker import Maze, MazeWalker

    maze = Maze.from_text(
        "\n".join(
            [
                "#######",
                "#S    #",
                "##### #",
                "#E    #",
                "#######",
            ]
        )
    )

    path = MazeWalker(maze).walk()

    assert path[0] == maze.start
    assert path[-1] == maze.exit
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        assert abs(x1 - x2) + abs(y1 - y2) == 1


def test_walled_off_exit_raises_no_path_error() -> None:
    """Test 8: An unreachable exit raises NoPathError"""
    from maze_walker import NoPathError, walk_maze

    maze = "\n".join(
        [
            "#####",
            "#S#E#",
            "#####",
        ]
    )

    with pytest.raises(NoPathError, match=r"^No path to exit$"):
        walk_maze(maze)


def test_diagonal_adjacency_is_not_a_connection() -> None:
    """Test 9: An exit touching the start only diagonally is unreachable"""
    from maze_walker import NoPathError, walk_maze

    maze = "\n".join(
        [
            "####",
            "#S##",
            "##E#",
            "####",
        ]
    )

    with pytest.raises(NoPathError, match="No path to exit"):
        walk_maze(maze)


def test_asterisks_are_walls_too() -> None:
    """Test 10: '*' cells block movement like '#'"""
    from maze_walker import NoPathError, walk_maze

    open_maze = "\n".join(
        [
            "*****",
            "*S E*",
            "*****",
        ]
    )
    assert walk_maze(open_maze) == [(1, 1), (2, 1), (3, 1)]

    blocked_maze = "\n".join(
        [
            "*****",
            "*S*E*",
            "*****",
        ]
    )
    with pytest.raises(NoPathError):
        walk_maze(blocked_maze)


def test_parsed_maze_exposes_dimensions_start_and_exit() -> None:
    """Test 11: Maze.from_text reports width, height, start and exit"""
    from maze_walker import Maze

    maze = Maze.from_text(
        "\n".join(
            [
                "#######",
                "#S   E#",
                "# ### #",
                "#     #",
                "#######",
            ]
        )
    )

    assert maze.width == 7
    assert maze.height == 5
    assert maze.start == (1, 1)
    assert maze.exit == (5, 1)
    assert maze.is_open(1, 1) is True
    assert maze.is_open(5, 1) is True
    assert maze.is_open(2, 1) is True
    assert maze.is_open(2, 2) is False


def test_maze_without_a_start_is_rejected() -> None:
    """Test 12: A maze missing 'S' raises ValueError"""
    from maze_walker import Maze

    with pytest.raises(ValueError, match=r"^Maze must contain exactly one start 'S'$"):
        Maze.from_text("####\n# E#\n####")


def test_maze_without_an_exit_is_rejected() -> None:
    """Test 13: A maze missing 'E' raises ValueError"""
    from maze_walker import Maze

    with pytest.raises(ValueError, match=r"^Maze must contain exactly one exit 'E'$"):
        Maze.from_text("####\n#S #\n####")


def test_maze_with_two_starts_is_rejected() -> None:
    """Test 14: A maze with duplicate 'S' markers raises ValueError"""
    from maze_walker import Maze

    with pytest.raises(ValueError, match=r"^Maze must contain exactly one start 'S'$"):
        Maze.from_text("#####\n#SSE#\n#####")


def test_maze_with_two_exits_is_rejected() -> None:
    """Test 15: A maze with duplicate 'E' markers raises ValueError"""
    from maze_walker import Maze

    with pytest.raises(ValueError, match=r"^Maze must contain exactly one exit 'E'$"):
        Maze.from_text("#####\n#SEE#\n#####")


def test_unknown_maze_characters_are_rejected() -> None:
    """Test 16: Characters outside the legend raise ValueError"""
    from maze_walker import Maze

    with pytest.raises(ValueError, match="Unknown maze character"):
        Maze.from_text("####\n#S?E\n####")


def test_walker_climbs_upward_toward_an_exit_above_the_start() -> None:
    """Test 17: A route leading straight up is walked cell by cell"""
    from maze_walker import walk_maze

    maze = "\n".join(
        [
            "###",
            "#E#",
            "# #",
            "#S#",
            "###",
        ]
    )

    assert walk_maze(maze) == [(1, 3), (1, 2), (1, 1)]


def test_only_surrounding_newlines_are_trimmed_not_spaces() -> None:
    """Test 18: Blank lines around the art are dropped; leading spaces keep
    their coordinates as corridor cells"""
    from maze_walker import walk_maze

    maze = "\n  S#\n##E#\n"

    assert walk_maze(maze) == [(2, 0), (2, 1)]


def test_unknown_characters_at_the_text_edges_are_rejected() -> None:
    """Test 19: Characters outside the legend are rejected even in the corners"""
    from maze_walker import Maze

    with pytest.raises(ValueError, match="Unknown maze character"):
        Maze.from_text("X###\n#SE#\n####")
