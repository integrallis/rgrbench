class Constants:
    MINE: int = -1


class MineFields:
    def __init__(self) -> None:
        self._fields: list[list[int]] = []

    def create(self, width: int, height: int) -> None:
        self._fields = [[0 for _ in range(height)] for _ in range(width)]

    def get_hint(self, x_pos: int, y_pos: int) -> int:
        return self._fields[x_pos][y_pos]

    def mine(self, x_pos: int, y_pos: int) -> None:
        self._fields[x_pos][y_pos] = Constants.MINE

        # Update all 8 adjacent cells
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip the mine cell itself
                nx, ny = x_pos + dx, y_pos + dy
                if (
                    0 <= nx < len(self._fields)
                    and 0 <= ny < len(self._fields[0])
                    and self._fields[nx][ny] != Constants.MINE
                ):
                    self._fields[nx][ny] += 1
