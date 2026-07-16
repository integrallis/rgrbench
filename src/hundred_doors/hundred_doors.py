"""100 Doors kata.

A row of doors, all starting closed, is visited in numbered passes. Pass k
toggles every k-th door (a closed door opens, an open door closes), and
there are exactly as many passes as there are doors. After the final pass a
door is open precisely when its 1-based position is a perfect square,
because only perfect squares have an odd number of divisors.

The final state can be reported three ways: as booleans (True for open), as
the 1-based positions of the open doors, or rendered as a string using "@"
for an open door and "#" for a closed one. Zero doors yields empty results;
a negative door count raises ValueError.

Kata catalogued at tddbuddy.com/katas/100-doors; implementation and tests
original (MIT), machine-authored from the specification, 2026.
"""


def final_door_states(count: int) -> list[bool]:
    """Return the state of each door after all passes (True means open)."""
    if count < 0:
        raise ValueError("door count must be non-negative")
    states = [False] * count
    for step in range(1, count + 1):
        for door in range(step - 1, count, step):
            states[door] = not states[door]
    return states


def open_doors(count: int) -> list[int]:
    """Return the 1-based positions of the doors left open after all passes."""
    return [
        position + 1
        for position, is_open in enumerate(final_door_states(count))
        if is_open
    ]


def render_doors(count: int) -> str:
    """Render the final door states as a string of "@" (open) and "#" (closed)."""
    return "".join("@" if is_open else "#" for is_open in final_door_states(count))
