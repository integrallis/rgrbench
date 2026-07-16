"""Greeting kata.

greet builds a greeting from a name, a list of names, or no name at all,
through progressive rules. A single name yields "Hello, <name>."; a missing
name (None or an empty list) yields "Hello, my friend.". A name written
entirely in uppercase is a shout and is answered in kind: "HELLO <NAME>!".
Two names are joined with "and"; three or more use commas with an Oxford
comma before the final "and". When normal and shouted names are mixed, the
normal greeting comes first, followed by the shouted greeting introduced
with "AND".

Two extensions from the kata are included: a list entry containing a comma
is split into separate names, unless the entry is wrapped in double quotes,
in which case the quotes are removed and the embedded comma is kept as part
of a single name.

Kata catalogued at tddbuddy.com/katas/greeting; implementation and tests
original (MIT), machine-authored from the specification, 2026.
"""


def greet(name: str | list[str] | None = None) -> str:
    """Return the greeting appropriate for the given name, names, or None."""
    if name is None:
        return "Hello, my friend."
    names = [name] if isinstance(name, str) else _expand(name)
    if not names:
        return "Hello, my friend."
    normal = [entry for entry in names if not entry.isupper()]
    shouted = [entry for entry in names if entry.isupper()]
    parts: list[str] = []
    if normal:
        parts.append(f"Hello, {_join(normal)}.")
    if shouted:
        shout = f"HELLO {_join(shouted).upper()}!"
        parts.append(f"AND {shout}" if normal else shout)
    return " ".join(parts)


def _expand(entries: list[str]) -> list[str]:
    """Split comma-separated entries into names; quoted entries stay whole."""
    names: list[str] = []
    for entry in entries:
        if len(entry) >= 2 and entry.startswith('"') and entry.endswith('"'):
            names.append(entry[1:-1])
        elif "," in entry:
            names.extend(part.strip() for part in entry.split(","))
        else:
            names.append(entry)
    return names


def _join(names: list[str]) -> str:
    """Join names with "and", using an Oxford comma for three or more."""
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return ", ".join(names[:-1]) + f", and {names[-1]}"
