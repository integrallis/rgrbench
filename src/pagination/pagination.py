"""Pagination calculator for splitting a collection of items into pages.

Given a non-negative total item count, a page size of at least one, and a
1-based requested page, the calculator produces: the total number of pages
(ceiling division), the validated current page (requests below 1 clamp to
the first page, requests beyond the last clamp to the last page), the
1-based indexes of the first and last items on the page, and flags telling
whether previous and next pages exist. An empty collection is a special
case: zero pages, no current page, and no items. A page window helper
returns the run of page numbers to display in a UI control: it is centred
on the current page where possible (for even window sizes the current page
sits just left of centre) and shifts to stay in range near either edge.

Kata catalogued at tddbuddy.com/katas/pagination; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Pagination:
    """Computed pagination facts for one page of a collection."""

    total_items: int
    page_size: int
    total_pages: int
    current_page: int
    start_item: int
    end_item: int
    has_previous: bool
    has_next: bool

    def page_window(self, window_size: int) -> list[int]:
        """Page numbers to display, centred on the current page when possible.

        The window shifts near the edges so it always stays within
        [1, total_pages]; if fewer pages exist than the window size, every
        page is returned. An empty collection yields an empty window.
        """
        if window_size < 1:
            raise ValueError(f"window_size must be at least 1, got [{window_size}]")
        if self.total_pages == 0:
            return []
        size = min(window_size, self.total_pages)
        start = self.current_page - (window_size - 1) // 2
        start = max(1, min(start, self.total_pages - size + 1))
        return list(range(start, start + size))


def paginate(total_items: int, page_size: int, current_page: int) -> Pagination:
    """Compute pagination facts for the requested page of a collection."""
    if total_items < 0:
        raise ValueError(f"total_items must be non-negative, got [{total_items}]")
    if page_size < 1:
        raise ValueError(f"page_size must be at least 1, got [{page_size}]")
    total_pages = -(-total_items // page_size)
    if total_pages == 0:
        return Pagination(
            total_items=total_items,
            page_size=page_size,
            total_pages=0,
            current_page=0,
            start_item=0,
            end_item=0,
            has_previous=False,
            has_next=False,
        )
    page = min(max(current_page, 1), total_pages)
    return Pagination(
        total_items=total_items,
        page_size=page_size,
        total_pages=total_pages,
        current_page=page,
        start_item=(page - 1) * page_size + 1,
        end_item=min(page * page_size, total_items),
        has_previous=page > 1,
        has_next=page < total_pages,
    )
