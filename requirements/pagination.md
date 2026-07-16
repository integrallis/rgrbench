# Page navigation for item collections

## Overview
A pagination service takes the size of an item collection, a page size, and a requested
page, and works out the page layout: how many pages exist, which items the current page
holds, whether neighbouring pages exist, and which page numbers to show in a navigation
window. Out-of-range page requests are clamped rather than refused, while nonsensical
sizes are rejected outright.

## User Stories

### US-1: Counting pages and locating items
As a user browsing a list, I want the collection divided into fixed-size pages with a known item range per page, so that I always know which slice of the list I am seeing.

- AC-1.1: The number of pages is the item count divided by the page size, rounded up:
  100 items at 10 per page make 10 pages, and 95 items at 10 per page also make 10
  pages, the last one partial.
- AC-1.2: Pages and items are numbered from 1, and the result reports the positions of
  the first and last items on the current page; page 3 at 10 per page covers items 21
  through 30.
- AC-1.3: On a final partial page the range ends at the last item; page 10 of 95 items
  at 10 per page covers items 91 through 95.
- AC-1.4: With a page size of 1, page n holds exactly item n and the page count equals
  the item count.
- AC-1.5: A collection smaller than one page fits entirely on page 1; 7 items at 10 per
  page make one page covering items 1 through 7, and a single item makes one page
  covering item 1 only.
- AC-1.6: The result also reports the total item count and page size it was computed
  from.

### US-2: Clamping out-of-range page requests
As a user following stale links, I want out-of-range page requests redirected to the nearest valid page, so that navigation never fails.

- AC-2.1: A requested page below 1, including zero and negative values, is clamped to
  page 1.
- AC-2.2: A requested page beyond the last page is clamped to the last page, which then
  reports its own item range.

### US-3: Knowing about neighbouring pages
As a user, I want to know whether previous and next pages exist, so that navigation controls can be enabled or disabled correctly.

- AC-3.1: The first page of a multi-page collection has a next page but no previous
  page.
- AC-3.2: An interior page has both a previous and a next page.
- AC-3.3: The last page has a previous page but no next page.
- AC-3.4: The only page of a single-page collection has neither neighbour.
- AC-3.5: Any page after page 1 reports that a previous page exists.

### US-4: Handling an empty collection
As a user of an empty list, I want a well-defined empty layout, so that the interface can render without special cases.

- AC-4.1: Zero items yield zero pages, a current page of 0, an item range of 0 through
  0, and no neighbouring pages, while still reporting the requested page size and the
  zero item count.
- AC-4.2: The page window of an empty collection is the empty list.

### US-5: Windowing page numbers for navigation
As a user, I want a short window of page numbers around the current page, so that a pager control can show nearby pages instead of all of them.

- AC-5.1: A window of odd width is centred on the current page; a 5-wide window around
  page 6 of 10 shows pages 4 through 8.
- AC-5.2: Near the first page the window anchors at page 1 instead of centring; a
  5-wide window around page 2 of 10 shows pages 1 through 5.
- AC-5.3: Near the last page the window anchors at the last page; a 5-wide window
  around page 10 of 10 shows pages 6 through 10.
- AC-5.4: A window wider than the page count lists every page; a 7-wide window over 3
  pages shows pages 1 through 3.
- AC-5.5: A window of even width places the current page just left of centre; a 4-wide
  window around page 6 of 10 shows pages 5 through 8.

### US-6: Rejecting invalid sizes
As an integrator, I want impossible inputs refused with precise messages, so that mistakes surface immediately.

- AC-6.1: A negative item count is rejected with an error naming the offending value in
  brackets; for -1 the message is exactly
  "total_items must be non-negative, got [-1]".
- AC-6.2: A page size below 1 is rejected the same way; for 0 the message is exactly
  "page_size must be at least 1, got [0]" and for -3 it is exactly
  "page_size must be at least 1, got [-3]".
- AC-6.3: A window width below 1 is rejected; for 0 the message is exactly
  "window_size must be at least 1, got [0]".

## Traceability
```json
{
  "test_exactly_divisible_collection_yields_even_pages": ["AC-1.1", "AC-1.2"],
  "test_remainder_items_add_a_final_partial_page": ["AC-1.1", "AC-1.3"],
  "test_middle_page_reports_its_item_range": ["AC-1.2"],
  "test_single_item_collection_has_one_page": ["AC-1.5", "AC-3.4"],
  "test_zero_items_is_a_special_empty_result": ["AC-4.1"],
  "test_current_page_below_one_clamps_to_first_page": ["AC-2.1"],
  "test_current_page_beyond_last_clamps_to_last_page": ["AC-2.2"],
  "test_first_page_has_next_but_no_previous": ["AC-3.1"],
  "test_middle_page_has_both_neighbours": ["AC-3.2"],
  "test_last_page_has_previous_but_no_next": ["AC-3.3"],
  "test_page_size_of_one_gives_one_item_per_page": ["AC-1.4"],
  "test_collection_smaller_than_one_page_fits_on_page_one": ["AC-1.5"],
  "test_negative_total_items_is_rejected": ["AC-6.1"],
  "test_page_size_below_one_is_rejected": ["AC-6.2"],
  "test_page_window_is_centred_on_the_current_page": ["AC-5.1"],
  "test_page_window_shifts_right_at_the_left_edge": ["AC-5.2"],
  "test_page_window_shifts_left_at_the_right_edge": ["AC-5.3"],
  "test_page_window_larger_than_page_count_returns_all_pages": ["AC-5.4"],
  "test_even_page_window_places_current_page_left_of_centre": ["AC-5.5"],
  "test_page_window_of_empty_collection_is_empty": ["AC-4.2"],
  "test_page_window_size_below_one_is_rejected": ["AC-6.3"],
  "test_empty_result_still_reports_item_count_and_page_size": ["AC-4.1", "AC-1.6"],
  "test_result_reports_the_total_item_count": ["AC-1.6"],
  "test_second_page_has_a_previous_page": ["AC-3.5"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
