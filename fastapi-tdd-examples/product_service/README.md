# Product Service - FastAPI TDD Port

This is a faithful port of the Spring Boot Product Service from `spring-junit-tdd` repository, implemented using strict Test-Driven Development (TDD) principles.

## Technology Stack
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Simple embedded database
- **Pytest**: Testing framework
- **Pydantic**: Data validation

## TDD Process

Following **RED-GREEN-REFACTOR** cycle, one test at a time:

1. **RED**: Write a failing test
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Improve code quality

### Refactoring Questions
- Can I make this better?
- Can I make this simpler?
- Is there an obvious design pattern that should be applied?
- Is this code obviously going to be a performance bottleneck?
- Is there an existing Python library that can do this?

## Test Progress

✅ **All 9 Tests Completed:**
1. Health check endpoint
2. GET /product/{id} - Found with ETag headers
3. GET /product/{id} - 404 Not Found
4. POST /product - Create with version 1
5. PUT /product/{id} - Update with version check
6. DELETE /product/{id} - Delete product successfully
7. PUT /product/{id} - Version conflict (409)
8. PUT /product/{id} - 404 when not found
9. DELETE /product/{id} - 404 when not found

✅ **Feature Complete!** All core CRUD operations with optimistic locking are implemented.

## Key Features Ported from Spring Boot

### Optimistic Locking
- Version field on Product model
- ETag headers using version number
- Version conflict detection (409 status)

### REST Best Practices
- Proper HTTP status codes (200, 201, 404, 409)
- Location headers for created/updated resources
- ETag headers for caching

### Database Integration
- SQLAlchemy ORM with SQLite
- Transaction management
- Proper connection handling

## Running the Tests

```bash
# Install dependencies
uv venv
uv sync

# Run all tests
uv run pytest tests/ -v

# Run specific test
uv run pytest tests/test_integration.py::test_create_product -v

# Run the application
uv run uvicorn src.main:app --reload
```

## API Endpoints

| Method | Endpoint | Description | Status |
|--------|----------|-------------|---------|
| GET | /health | Health check | ✅ |
| GET | /product/{id} | Get product by ID | ✅ |
| POST | /product | Create new product | ✅ |
| PUT | /product/{id} | Update product with version | ✅ |
| DELETE | /product/{id} | Delete product | ✅ |

## Differences from Spring Boot

1. **Async by default**: FastAPI uses async/await
2. **Type hints**: Python type annotations instead of Java types
3. **Pydantic**: Automatic validation and serialization
4. **SQLite**: Simpler than H2 for testing
5. **No mocking in integration tests**: Using real database

## TDD Lessons Learned

1. **Start simple**: Health check first
2. **One test at a time**: Never write multiple tests before implementation
3. **Minimal code**: Just enough to pass the test
4. **Refactor continuously**: Improve after each green test
5. **Real database**: Integration tests are more valuable than mocked tests

## Next Steps

- Complete remaining CRUD operations
- Add optimistic locking for updates
- Implement version conflict handling
- Add more comprehensive error handling
- Consider adding service layer for business logic
