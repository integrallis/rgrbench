# Todo management web service

## Overview
An HTTP service for managing a personal todo list. Clients create, read, update, and delete
todo items over a JSON API; items carry a title, a completion flag, and optional due date
and priority attributes; the collection can be filtered by completion status. The service
reports its own health.

## User Stories

### US-1: Service health
As an operator, I want a health endpoint, so that I can verify the service is up.

- AC-1.1: A health request succeeds and reports the service as healthy.

### US-2: Manage todo items
As a user, I want to create, view, update, and delete todos, so that I can track my tasks.

- AC-2.1: The list starts empty and a list request succeeds.
- AC-2.2: Creating a todo returns a created status with a numeric identifier (numbered from 1), the given title, and an incomplete state.
- AC-2.3: A todo can be fetched by its identifier, returning its title and state.
- AC-2.4: Updating a todo changes its title and completion state and returns the updated item.
- AC-2.5: Deleting a todo succeeds with a no-content status, after which fetching it reports not-found.
- AC-2.6: Fetching or updating a nonexistent todo reports not-found with a detail message mentioning that it was not found.

### US-3: Enrich and filter todos
As a user, I want optional due dates and priorities and status filtering, so that I can organize my work.

- AC-3.1: A todo may be created with a due date, which is stored and returned as given.
- AC-3.2: A todo may be created with a priority, which is stored and returned as given.
- AC-3.3: The list can be filtered by completion status, returning only matching items.

## Traceability
```json
{
  "test_health_check_returns_200": ["AC-1.1"],
  "test_get_todos_returns_empty_list": ["AC-2.1"],
  "test_create_todo": ["AC-2.2"],
  "test_get_todo_by_id": ["AC-2.3"],
  "test_update_todo": ["AC-2.4"],
  "test_delete_todo": ["AC-2.5"],
  "test_get_nonexistent_todo_returns_404": ["AC-2.6"],
  "test_update_nonexistent_todo_returns_404": ["AC-2.6"],
  "test_create_todo_with_due_date": ["AC-3.1"],
  "test_create_todo_with_priority": ["AC-3.2"],
  "test_filter_todos_by_status": ["AC-3.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
