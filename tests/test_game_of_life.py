"""
Tests for the Game of Life kata.
Underpopulation, survival, overpopulation, reproduction, and classic patterns
on an unbounded plane.
"""


def test_empty_grid_has_no_live_cells() -> None:
    """Test 1: A grid built with no cells has population zero"""
    from game_of_life import Grid

    grid = Grid()

    assert grid.population == 0
    assert grid.live_cells == frozenset()


def test_empty_grid_stays_empty() -> None:
    """Test 2: Nothing is born on an empty grid"""
    from game_of_life import Grid

    grid = Grid()

    assert grid.next_generation() == Grid()


def test_lone_cell_dies_of_underpopulation() -> None:
    """Test 3: A live cell with zero live neighbours dies"""
    from game_of_life import Grid

    grid = Grid([(0, 0)])

    assert grid.next_generation().is_alive(0, 0) is False


def test_pair_of_cells_dies_of_underpopulation() -> None:
    """Test 4: Two adjacent live cells each have one neighbour and both die"""
    from game_of_life import Grid

    grid = Grid([(0, 0), (1, 0)])

    next_grid = grid.next_generation()
    assert next_grid.is_alive(0, 0) is False
    assert next_grid.is_alive(1, 0) is False


def test_live_cell_with_two_neighbours_survives() -> None:
    """Test 5: The centre of a row of three survives with two neighbours"""
    from game_of_life import Grid

    grid = Grid([(0, 0), (1, 0), (2, 0)])

    assert grid.next_generation().is_alive(1, 0) is True


def test_live_cell_with_three_neighbours_survives() -> None:
    """Test 6: Every cell of a 2x2 block has three neighbours and survives"""
    from game_of_life import Grid

    grid = Grid([(0, 0), (1, 0), (0, 1), (1, 1)])

    next_grid = grid.next_generation()
    assert next_grid.is_alive(0, 0) is True
    assert next_grid.is_alive(1, 1) is True


def test_live_cell_with_four_neighbours_dies_of_overpopulation() -> None:
    """Test 7: The centre of a plus shape has four neighbours and dies"""
    from game_of_life import Grid

    grid = Grid([(1, 1), (0, 1), (2, 1), (1, 0), (1, 2)])

    assert grid.next_generation().is_alive(1, 1) is False


def test_dead_cell_with_three_neighbours_is_born() -> None:
    """Test 8: A dead cell with exactly three live neighbours becomes alive"""
    from game_of_life import Grid

    grid = Grid([(0, 0), (1, 0), (0, 1)])

    assert grid.is_alive(1, 1) is False
    assert grid.next_generation().is_alive(1, 1) is True


def test_dead_cell_with_two_neighbours_stays_dead() -> None:
    """Test 9: Two live neighbours are not enough for reproduction"""
    from game_of_life import Grid

    grid = Grid([(0, 0), (2, 0)])

    assert grid.next_generation().is_alive(1, 0) is False


def test_block_still_life_is_stable() -> None:
    """Test 10: The 2x2 block reproduces itself exactly"""
    from game_of_life import Grid

    block = Grid([(0, 0), (1, 0), (0, 1), (1, 1)])

    assert block.next_generation() == block


def test_beehive_still_life_is_stable() -> None:
    """Test 11: The beehive reproduces itself exactly"""
    from game_of_life import Grid

    beehive = Grid([(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)])

    assert beehive.next_generation() == beehive


def test_blinker_flips_from_vertical_to_horizontal() -> None:
    """Test 12: A vertical blinker becomes horizontal in one generation"""
    from game_of_life import Grid

    vertical = Grid([(1, 0), (1, 1), (1, 2)])
    horizontal = Grid([(0, 1), (1, 1), (2, 1)])

    assert vertical.next_generation() == horizontal


def test_blinker_oscillates_with_period_two() -> None:
    """Test 13: A blinker returns to its original shape after two generations"""
    from game_of_life import Grid

    blinker = Grid([(1, 0), (1, 1), (1, 2)])

    assert blinker.next_generation().next_generation() == blinker


def test_toad_oscillates_with_period_two() -> None:
    """Test 14: The toad changes shape then returns after two generations"""
    from game_of_life import Grid

    toad = Grid([(1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2)])

    step_one = toad.next_generation()
    assert step_one != toad
    assert step_one.next_generation() == toad


def test_glider_translates_diagonally_every_four_generations() -> None:
    """Test 15: After four generations the glider is shifted by (1, 1)"""
    from game_of_life import Grid

    cells = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
    grid = Grid(cells)

    for _ in range(4):
        grid = grid.next_generation()

    assert grid == Grid([(x + 1, y + 1) for x, y in cells])


def test_from_rows_builds_grid_from_text_pattern() -> None:
    """Test 16: from_rows maps rows to y and columns to x"""
    from game_of_life import Grid

    grid = Grid.from_rows([".*.", "..*", "***"])

    assert grid == Grid([(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)])


def test_render_displays_window_of_the_plane() -> None:
    """Test 17: render draws live cells as '*' and dead cells as '.'"""
    from game_of_life import Grid

    blinker = Grid([(1, 0), (1, 1), (1, 2)])

    assert blinker.render(3, 3) == ".*.\n.*.\n.*."


def test_render_round_trips_with_from_rows() -> None:
    """Test 18: A pattern parsed from rows renders back to the same rows"""
    from game_of_life import Grid

    rows = ["**.", "*..", "..*"]
    grid = Grid.from_rows(rows)

    assert grid.render(3, 3) == "\n".join(rows)


def test_next_generation_does_not_mutate_original_grid() -> None:
    """Test 19: Grids are immutable; stepping returns a new grid"""
    from game_of_life import Grid

    original = Grid([(0, 0)])
    original.next_generation()

    assert original.live_cells == frozenset({(0, 0)})


def test_live_neighbours_counts_all_eight_surrounding_cells() -> None:
    """Test 20: Neighbour count includes diagonals and only the eight adjacent cells"""
    from game_of_life import Grid

    block = Grid([(0, 0), (1, 0), (0, 1), (1, 1)])

    assert block.live_neighbours(0, 0) == 3
    assert block.live_neighbours(2, 2) == 1
    assert block.live_neighbours(5, 5) == 0


def test_cells_far_from_any_pattern_are_dead() -> None:
    """Test 21: The plane is unbounded and defaults to dead everywhere"""
    from game_of_life import Grid

    grid = Grid([(0, 0)])

    assert grid.is_alive(1_000_000, -1_000_000) is False


def test_grids_with_same_cells_are_equal_and_hash_alike() -> None:
    """Test 22: Equality and hashing depend only on the live cell set"""
    from game_of_life import Grid

    first = Grid([(0, 0), (1, 1)])
    second = Grid([(1, 1), (0, 0)])

    assert first == second
    assert hash(first) == hash(second)


def test_hash_varies_with_the_live_cell_set() -> None:
    """Test 23: Hashing depends on the live cell set, so distinct grids do not all collide"""
    from game_of_life import Grid

    hashes = {hash(Grid([(i, 0)])) for i in range(8)}

    assert len(hashes) > 1
