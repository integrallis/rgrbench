class RecentlyUsedList:
    """Port of C# RecentlyUsedList"""

    def __init__(self, size: int | None = None) -> None:
        self._items: list[str] = []
        self._size = size if size is not None else 5  # Default size is 5

    def add(self, item: str | None) -> None:
        """Add an item to the list - most recent first, no duplicates, respects size limit"""
        if item is None:
            raise ValueError(
                "List items should not be Empty or Null. But it was [None]"
            )
        if item == "":
            raise ValueError("List items should not be Empty or Null. But it was []")
        if item in self._items:
            self._items.remove(item)
        self._items.insert(0, item)
        # Trim to size limit
        if len(self._items) > self._size:
            self._items = self._items[: self._size]

    def count(self) -> int:
        """Return the count of items in the list"""
        return len(self._items)

    def to_list(self) -> list[str]:
        """Return the list of items"""
        return self._items.copy()

    def get_list_item(self, index: int) -> str:
        """Get an item from the list by index"""
        if index < 0:
            raise ValueError(
                f"supplied index [{index}] should be non-negative and not greater than [{len(self._items) - 1}]."
            )
        if index >= len(self._items):
            raise ValueError(
                f"supplied index [{index}] should not greater than [{len(self._items) - 1}]."
            )
        return self._items[index]

    @property
    def size(self) -> int:
        """Get the maximum size of the list"""
        return self._size
